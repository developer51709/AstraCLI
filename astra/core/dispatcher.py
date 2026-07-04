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

def dispatch(command, args):
    if command == "ask":
        prompt = " ".join(args)
        provider = provider_manager.get_active_provider()
        model = model_manager.get_active_model()
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
        plugin_loader.handle_cli(args)
        return

    print(f"AstraCLI: Unknown command '{command}'")
