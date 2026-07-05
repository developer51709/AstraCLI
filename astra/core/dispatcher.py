from astra.core.provider_manager import ProviderManager
from astra.core.model_manager import ModelManager
from astra.core.plugin_loader import PluginLoader
from astra.core.credential_manager import CredentialManager
from astra.core.updater import Updater

provider_manager = ProviderManager()
model_manager = ModelManager()
plugin_loader = PluginLoader()
credentials = CredentialManager()
updater = Updater()

def _print_help():
    print("AstraCLI command reference:")
    print("  astra ask [--provider name] [--model name] <prompt>")
    print("  astra providers")
    print("  astra providers set <name>")
    print("  astra models")
    print("  astra models set <name>")
    print("  astra plugins")
    print("  astra plugins run <plugin> [args...]")
    print("  astra creds")
    print("  astra creds add <provider> <key>")
    print("  astra creds remove <provider>")
    print("  astra update")
    print("  astra help")


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
            print("AstraCLI: ask command requires a prompt.")
            return

        provider = (
            provider_manager.get_provider(provider_name, credentials.creds)
            if provider_name
            else provider_manager.get_active_provider(credentials.creds)
        )
        if provider is None:
            print("AstraCLI: No provider available.")
            return

        model = model_manager.get_model(model_name) if model_name else model_manager.get_active_model()
        if model is None:
            print("AstraCLI: No model available.")
            return

        output = provider.generate(prompt, model)
        print(output)
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

    print(f"AstraCLI: Unknown command '{command}'")
