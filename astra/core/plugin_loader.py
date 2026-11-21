import os
import importlib
from astra.utils import logger


class PluginLoader:
    def __init__(self):
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        folder = os.path.join(os.path.dirname(__file__), "..", "plugins")
        if not os.path.isdir(folder):
            return

        for file in sorted(os.listdir(folder)):
            if not file.endswith(".py") or file == "__init__.py":
                continue

            name = file[:-3]
            try:
                module = importlib.import_module(f"astra.plugins.{name}")
            except Exception as exc:
                logger.warn(f"Skipping plugin '{name}': {exc}")
                continue

            if hasattr(module, "run"):
                self.plugins[name] = module.run
            else:
                logger.warn(f"Skipping plugin '{name}': no run() function.")

    def handle_cli(self, args, context=None):
        if not args:
            logger.info("Plugins: " + (", ".join(sorted(self.plugins)) if self.plugins else "(none)"))
            return 0

        if args[0] == "run":
            if len(args) < 2:
                logger.info("Usage: astra plugins run <plugin> [args...]")
                return 1

            plugin = args[1]
            if plugin not in self.plugins:
                logger.error("Plugin not found.")
                return 1

            plugin_context = dict(context or {})
            plugin_context["args"] = args[2:]
            try:
                result = self.plugins[plugin](plugin_context)
            except Exception as exc:
                logger.error(f"Plugin {plugin} failed: {exc}")
                return 1

            logger.info(result)
            return 0

        logger.error("AstraCLI: Unknown plugins command")
        return 1
