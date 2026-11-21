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
    logger.info("  astra creds add <provider>")
    logger.info("  astra creds get <provider>")
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
    """Run one command and return a process exit status (0 = success)."""
    if command in ("help", "-h", "--help"):
        _print_help()
        return 0

    if command == "ask":
        provider_name, model_name, prompt = _parse_ask_args(args)
        if not prompt:
            logger.error("AstraCLI: ask command requires a prompt.")
            return 1

        if provider_name and provider_name not in provider_manager.providers:
            available = ", ".join(sorted(provider_manager.providers)) or "(none)"
            logger.error(f"AstraCLI: unknown provider '{provider_name}'. Available: {available}")
            return 1

        provider = (
            provider_manager.get_provider(provider_name, credentials.creds)
            if provider_name
            else provider_manager.get_active_provider(credentials.creds)
        )
        if provider is None:
            logger.error("AstraCLI: No provider available.")
            return 1

        if not getattr(provider, "configured", True):
            name = provider_name or provider_manager.active_provider
            needed = provider_manager.credential_name(name)
            logger.error(
                f"AstraCLI: provider '{name}' has no API key. "
                f"Run 'astra creds add {needed}' and try again."
            )
            return 1

        model = model_manager.get_model(model_name) if model_name else model_manager.get_active_model()
        if model is None:
            logger.error("AstraCLI: No model available.")
            return 1

        output = provider.generate(prompt, model)
        logger.info(output)
        return 0

    if command == "update":
        return updater.update()

    if command == "creds":
        return credentials.handle_cli(args)

    if command == "providers":
        return provider_manager.handle_cli(args)

    if command == "models":
        return model_manager.handle_cli(args)

    if command == "plugins":
        context = {
            "provider": provider_manager.active_provider,
            "model": model_manager.active_model,
            "credentials": credentials.creds,
        }
        return plugin_loader.handle_cli(args, context)

    logger.error(f"AstraCLI: Unknown command '{command}'")
    return 1
