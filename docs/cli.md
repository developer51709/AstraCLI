# AstraCLI CLI Reference

## Commands

### `astra ask`
Send a prompt to the active AI provider and model.

Usage:
```bash
astra ask [--provider name] [--model name] <prompt>
```

Examples:
```bash
astra ask "Explain this Python error."
astra ask --provider ollama --model llama3.1-8b "Summarize this log."
```

### `astra providers`
List available providers and show the active provider.

Usage:
```bash
astra providers
astra providers set <name>
```

### `astra models`
List available models and show the active model.

Usage:
```bash
astra models
astra models set <name>
```

### `astra plugins`
List and run plugins.

Usage:
```bash
astra plugins
astra plugins run <plugin> [args...]
```

### `astra creds`
Manage stored credentials. `add` prompts for the key instead of taking it on
the command line, and `get` only shows a masked value.

Usage:
```bash
astra creds
astra creds add <provider>
astra creds get <provider>
astra creds remove <provider>
```

### `astra update`
Fetch the latest changes from the repository using git.

Usage:
```bash
astra update
```
