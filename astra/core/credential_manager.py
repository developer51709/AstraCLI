import os
import json

class CredentialManager:
    def __init__(self):
        self.path = os.path.expanduser("~/.astra/credentials.json")
        self.creds = {}
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                try:
                    self.creds = json.load(f)
                except json.JSONDecodeError:
                    self.creds = {}

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.creds, f, indent=2)

    def handle_cli(self, args):
        if not args or args[0] in ("list", "show"):
            if self.creds:
                print("Stored credentials:", ", ".join(self.creds.keys()))
            else:
                print("No stored credentials.")
            return

        if args[0] == "add":
            if len(args) < 3:
                print("Usage: astra creds add <provider> <key>")
                return

            provider = args[1]
            key = args[2]
            self.creds[provider] = key
            self.save()
            print(f"Credential added for {provider}")
            return

        if args[0] in ("remove", "rm"):
            if len(args) < 2:
                print("Usage: astra creds remove <provider>")
                return

            provider = args[1]
            if provider in self.creds:
                del self.creds[provider]
                self.save()
                print(f"Credential removed for {provider}")
            else:
                print("No credential found for", provider)
            return

        if args[0] == "get":
            if len(args) < 2:
                print("Usage: astra creds get <provider>")
                return

            provider = args[1]
            print(self.creds.get(provider, "No credential stored for this provider."))
            return

        print("AstraCLI: Unknown creds command")
