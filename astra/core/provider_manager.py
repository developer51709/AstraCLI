import os
import importlib
from astra.core.config import load_config, update_config
from astra.utils import logger

DEFAULT_PROVIDER = "ollama"


class ProviderManager:
    def __init__(self):
        self.providers = {}
        self.credential_keys = {}
        self.active_provider = None
        self.load_providers()
        self.load_active_provider()

    def load_providers(self):
        folder = os.path.join(os.path.dirname(__file__), "..", "providers")
        if not os.path.isdir(folder):
            return

        for file in sorted(os.listdir(folder)):
            if not file.endswith(".py") or file == "__init__.py":
                continue

            name = file[:-3]
            try:
                module = importlib.import_module(f"astra.providers.{name}")
            except Exception as exc:
                logger.warn(f"Skipping provider '{name}': {exc}")
                continue

            if not hasattr(module, "Provider"):
                logger.warn(f"Skipping provider '{name}': no Provider class.")
                continue

            self.providers[name] = module.Provider
            self.credential_keys[name] = tuple(getattr(module, "CREDENTIAL_KEYS", (name,)))

        if self.providers and self.active_provider is None:
            self.active_provider = self._default_provider()

    def _default_provider(self):
        if DEFAULT_PROVIDER in self.providers:
            return DEFAULT_PROVIDER
        return sorted(self.providers)[0]

    def load_active_provider(self):
        config = load_config()
        name = config.get("active_provider")
        if name in self.providers:
            self.active_provider = name
        elif name:
            logger.warn(
                f"Configured provider '{name}' is not available; "
                f"using '{self.active_provider}'."
            )

    def save_active_provider(self):
        if self.active_provider:
            update_config({"active_provider": self.active_provider})

    def get_provider(self, name, credentials=None):
        """Build a provider with only the credentials it declares it uses."""
        if name not in self.providers:
            return None

        stored = credentials or {}
        keys = self.credential_keys.get(name) or (name,)
        match = next((key for key in keys if key in stored), None)
        scoped = {keys[0]: stored[match]} if match else {}
        return self.providers[name](scoped)

    def credential_name(self, name):
        """The canonical stored name a provider's key is read from."""
        keys = self.credential_keys.get(name) or (name,)
        return keys[0]

    def get_active_provider(self, credentials=None):
        if self.active_provider is None:
            return None
        return self.get_provider(self.active_provider, credentials)

    def handle_cli(self, args):
        if not args:
            logger.info("Providers: " + (", ".join(sorted(self.providers)) if self.providers else "(none)"))
            logger.info("Active: " + (self.active_provider or "(none)"))
            return 0

        if args[0] in ("set", "use"):
            if len(args) < 2:
                logger.info("Usage: astra providers set <name>")
                return 1

            name = args[1]
            if name in self.providers:
                self.active_provider = name
                self.save_active_provider()
                logger.success(f"Active provider set to {name}")
                return 0

            logger.error("Provider not found.")
            return 1

        if args[0] in ("active", "current"):
            logger.info("Active provider: " + (self.active_provider or "(none)"))
            return 0

        logger.error("AstraCLI: Unknown providers command")
        return 1
