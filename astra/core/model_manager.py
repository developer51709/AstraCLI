import os
import yaml

class ModelManager:
    def __init__(self):
        self.models = {}
        self.active_model = None
        self.load_models()

    def load_models(self):
        folder = os.path.join(os.path.dirname(__file__), "..", "models")
        for file in os.listdir(folder):
            if file.endswith(".yaml"):
                path = os.path.join(folder, file)
                with open(path, "r") as f:
                    data = yaml.safe_load(f)
                    self.models[data["name"]] = data
        if self.models:
            self.active_model = list(self.models.keys())[0]

    def get_active_model(self):
        return self.models[self.active_model]

    def handle_cli(self, args):
        if not args:
            print("Models:", ", ".join(self.models.keys()))
            print("Active:", self.active_model)
            return

        if args[0] == "set":
            name = args[1]
            if name in self.models:
                self.active_model = name
                print(f"Active model set to {name}")
            else:
                print("Model not found.")
