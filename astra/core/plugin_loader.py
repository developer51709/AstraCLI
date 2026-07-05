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

        for file in os.listdir(folder):
            if file.endswith(".py") and file != "__init__.py":
                name = file[:-3]
                module = importlib.import_module(f"astra.plugins.{name}")
                if hasattr(module, "run"):
                    self.plugins[name] = module.run

    def handle_cli(self, args, context=None):
        if not args:
            logger.info("Plugins: " + (", ".join(self.plugins.keys()) if self.plugins else "(none)"))
            return

        if args[0] == "run":
            if len(args) < 2:
                logger.info("Usage: astra plugins run <plugin> [args...]")
                return

            plugin = args[1]
            if plugin in self.plugins:
                plugin_context = context or {}
                plugin_context["args"] = args[2:]
                try:
                    result = self.plugins[plugin](plugin_context)
                    logger.info(result)
                except Exception as exc:
                    logger.error(f"Plugin {plugin} failed: {exc}")
            else:
                logger.error("Plugin not found.")
            return

        logger.error("AstraCLI: Unknown plugins command")
