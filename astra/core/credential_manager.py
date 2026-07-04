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
                self.creds = json.load(f)

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.creds, f, indent=2)

    def handle_cli(self, args):
        if not args:
            print("Stored credentials:", ", ".join(self.creds.keys()))
            return

        if args[0] == "add":
            provider = args[1]
            key = args[2]
            self.creds[provider] = key
            self.save()
            print(f"Credential added for {provider}")
            return

        if args[0] == "remove":
            provider = args[1]
            if provider in self.creds:
                del self.creds[provider]
                self.save()
                print(f"Credential removed for {provider}")
            return
