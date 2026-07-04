import os
import importlib

class PluginLoader:
    def __init__(self):
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        folder = os.path.join(os.path.dirname(__file__), "..", "plugins")
        for file in os.listdir(folder):
            if file.endswith(".py") and file != "__init__.py":
                name = file[:-3]
                module = importlib.import_module(f"astra.plugins.{name}")
                if hasattr(module, "run"):
                    self.plugins[name] = module.run

    def handle_cli(self, args):
        if not args:
            print("Plugins:", ", ".join(self.plugins.keys()))
            return

        if args[0] == "run":
            plugin = args[1]
            if plugin in self.plugins:
                print(self.plugins[plugin]({}))
            else:
                print("Plugin not found.")
