import os
import importlib

class ProviderManager:
    def __init__(self):
        self.providers = {}
        self.active_provider = None
        self.load_providers()

    def load_providers(self):
        folder = os.path.join(os.path.dirname(__file__), "..", "providers")
        for file in os.listdir(folder):
            if file.endswith(".py") and file != "__init__.py":
                name = file[:-3]
                module = importlib.import_module(f"astra.providers.{name}")
                if hasattr(module, "Provider"):
                    self.providers[name] = module.Provider
        if self.providers:
            self.active_provider = list(self.providers.keys())[0]

    def get_active_provider(self):
        provider_class = self.providers[self.active_provider]
        return provider_class({})

    def handle_cli(self, args):
        if not args:
            print("Providers:", ", ".join(self.providers.keys()))
            print("Active:", self.active_provider)
            return

        if args[0] == "set":
            name = args[1]
            if name in self.providers:
                self.active_provider = name
                print(f"Active provider set to {name}")
            else:
                print("Provider not found.")
