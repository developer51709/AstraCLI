import os
import json
import getpass
from astra.utils import logger

FILE_MODE = 0o600


class CredentialManager:
    def __init__(self):
        self.path = os.path.expanduser("~/.astra/credentials.json")
        self.creds = {}
        self.load()

    def load(self):
        if not os.path.exists(self.path):
            return

        try:
            with open(self.path, "r") as f:
                self.creds = json.load(f) or {}
        except (json.JSONDecodeError, OSError):
            self.creds = {}
            return

        # Repair stores written before the file mode was enforced.
        try:
            if os.stat(self.path).st_mode & 0o077:
                os.chmod(self.path, FILE_MODE)
        except OSError:
            pass

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        tmp = self.path + ".tmp"

        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, FILE_MODE)
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(self.creds, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, self.path)
        except OSError:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise

        os.chmod(self.path, FILE_MODE)

    @staticmethod
    def _prompt_key(provider):
        try:
            return getpass.getpass(f"API key for {provider}: ").strip()
        except (EOFError, KeyboardInterrupt):
            return ""

    def handle_cli(self, args):
        if not args or args[0] in ("list", "show"):
            if self.creds:
                logger.info("Stored credentials: " + ", ".join(sorted(self.creds)))
            else:
                logger.info("No stored credentials.")
            return 0

        if args[0] == "add":
            if len(args) < 2:
                logger.error("Usage: astra creds add <provider>")
                return 1

            provider = args[1]
            if len(args) > 2:
                logger.warn(
                    "Ignoring the key passed on the command line: it would be "
                    "saved in shell history and visible in the process list."
                )

            key = self._prompt_key(provider)
            if not key:
                logger.error("No key provided.")
                return 1

            self.creds[provider] = key
            self.save()
            logger.success(f"Credential added for {provider}")
            return 0

        if args[0] in ("remove", "rm"):
            if len(args) < 2:
                logger.info("Usage: astra creds remove <provider>")
                return 1

            provider = args[1]
            if provider in self.creds:
                del self.creds[provider]
                self.save()
                logger.success(f"Credential removed for {provider}")
                return 0

            logger.error("No credential found for " + provider)
            return 1

        if args[0] == "get":
            if len(args) < 2:
                logger.info("Usage: astra creds get <provider>")
                return 1

            provider = args[1]
            key = self.creds.get(provider)
            if key is None:
                logger.error("No credential stored for " + provider)
                return 1

            key = str(key)
            masked = f"****{key[-4:]}" if len(key) > 8 else "****"
            logger.info(f"{provider}: {masked}")
            return 0

        logger.error("AstraCLI: Unknown creds command")
        return 1
