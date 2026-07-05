from astra.core.provider_manager import ProviderManager
from astra.core.model_manager import ModelManager
from astra.core.plugin_loader import PluginLoader
from astra.core.credential_manager import CredentialManager
from astra.core.updater import Updater
from astra.utils import logger

provider_manager = ProviderManager()
model_manager = ModelManager()
plugin_loader = PluginLoader()
credentials = CredentialManager()
updater = Updater()

def _print_help():
    logger.info("AstraCLI command reference:")
    logger.info("  astra ask [--provider name] [--model name] <prompt>")
    logger.info("  astra providers")
    logger.info("  astra providers set <name>")
    logger.info("  astra models")
    logger.info("  astra models set <name>")
    logger.info("  astra plugins")
    logger.info("  astra plugins run <plugin> [args...]")
    logger.info("  astra creds")
    logger.info("  astra creds add <provider> <key>")
    logger.info("  astra creds remove <provider>")
    logger.info("  astra update")
    logger.info("  astra help")


def _parse_ask_args(args):
    provider_name = None
    model_name = None
    idx = 0

    while idx < len(args):
        if args[idx] in ("--provider", "-p") and idx + 1 < len(args):
            provider_name = args[idx + 1]
            idx += 2
            continue
        if args[idx] in ("--model", "-m") and idx + 1 < len(args):
            model_name = args[idx + 1]
            idx += 2
            continue
        break

    prompt = " ".join(args[idx:])
    return provider_name, model_name, prompt


def dispatch(command, args):
    if command in ("help", "-h", "--help"):
        _print_help()
        return

    if command == "ask":
        provider_name, model_name, prompt = _parse_ask_args(args)
        if not prompt:
            logger.error("AstraCLI: ask command requires a prompt.")
            return

        provider = (
            provider_manager.get_provider(provider_name, credentials.creds)
            if provider_name
            else provider_manager.get_active_provider(credentials.creds)
        )
        if provider is None:
            logger.error("AstraCLI: No provider available.")
            return

        model = model_manager.get_model(model_name) if model_name else model_manager.get_active_model()
        if model is None:
            logger.error("AstraCLI: No model available.")
            return

        output = provider.generate(prompt, model)
        logger.info(output)
        return

    if command == "update":
        updater.update()
        return

    if command == "creds":
        credentials.handle_cli(args)
        return

    if command == "providers":
        provider_manager.handle_cli(args)
        return

    if command == "models":
        model_manager.handle_cli(args)
        return

    if command == "plugins":
        context = {
            "provider": provider_manager.active_provider,
            "model": model_manager.active_model,
            "credentials": credentials.creds,
        }
        plugin_loader.handle_cli(args, context)
        return

    logger.error(f"AstraCLI: Unknown command '{command}'")
