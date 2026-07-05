import os
import importlib
from astra.core.config import load_config, update_config

class ProviderManager:
    def __init__(self):
        self.providers = {}
        self.active_provider = None
        self.load_providers()
        self.load_active_provider()

    def load_providers(self):
        folder = os.path.join(os.path.dirname(__file__), "..", "providers")
        if not os.path.isdir(folder):
            return

        for file in os.listdir(folder):
            if file.endswith(".py") and file != "__init__.py":
                name = file[:-3]
                module = importlib.import_module(f"astra.providers.{name}")
                if hasattr(module, "Provider"):
                    self.providers[name] = module.Provider

        if self.providers and self.active_provider is None:
            self.active_provider = list(self.providers.keys())[0]

    def load_active_provider(self):
        config = load_config()
        name = config.get("active_provider")
        if name in self.providers:
            self.active_provider = name

    def save_active_provider(self):
        if self.active_provider:
            update_config({"active_provider": self.active_provider})

    def get_provider(self, name, credentials=None):
        if name not in self.providers:
            return None
        provider_class = self.providers[name]
        return provider_class(credentials or {})

    def get_active_provider(self, credentials=None):
        if self.active_provider is None:
            return None
        return self.get_provider(self.active_provider, credentials)

    def handle_cli(self, args):
        if not args:
            print("Providers:", ", ".join(self.providers.keys()) if self.providers else "(none)")
            print("Active:", self.active_provider or "(none)")
            return

        if args[0] in ("set", "use"):
            if len(args) < 2:
                print("Usage: astra providers set <name>")
                return

            name = args[1]
            if name in self.providers:
                self.active_provider = name
                self.save_active_provider()
                print(f"Active provider set to {name}")
            else:
                print("Provider not found.")
            return

        if args[0] in ("active", "current"):
            print("Active provider:", self.active_provider or "(none)")
            return

        print("AstraCLI: Unknown providers command")
