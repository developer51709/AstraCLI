import os
import yaml
from astra.core.config import load_config, update_config

class ModelManager:
    def __init__(self):
        self.models = {}
        self.active_model = None
        self.load_models()
        self.load_active_model()

    def load_models(self):
        folder = os.path.join(os.path.dirname(__file__), "..", "models")
        if not os.path.isdir(folder):
            return

        for file in os.listdir(folder):
            if file.endswith(".yaml"):
                path = os.path.join(folder, file)
                with open(path, "r") as f:
                    data = yaml.safe_load(f) or {}
                    if isinstance(data, dict) and data.get("name"):
                        self.models[data["name"]] = data

        if self.models and self.active_model is None:
            self.active_model = list(self.models.keys())[0]

    def load_active_model(self):
        config = load_config()
        name = config.get("active_model")
        if name in self.models:
            self.active_model = name

    def save_active_model(self):
        if self.active_model:
            update_config({"active_model": self.active_model})

    def get_model(self, name):
        return self.models.get(name)

    def get_active_model(self):
        return self.get_model(self.active_model)

    def handle_cli(self, args):
        if not args:
            print("Models:", ", ".join(self.models.keys()) if self.models else "(none)")
            print("Active:", self.active_model or "(none)")
            return

        if args[0] == "set":
            if len(args) < 2:
                print("Usage: astra models set <name>")
                return

            name = args[1]
            if name in self.models:
                self.active_model = name
                self.save_active_model()
                print(f"Active model set to {name}")
            else:
                print("Model not found.")
            return

        print("AstraCLI: Unknown models command")
