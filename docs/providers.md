# AstraCLI Providers

AstraCLI loads provider implementations from `astra/providers/` automatically.

## Adding a new provider

Create a new file in `astra/providers/` with a `Provider` class:

```python
class Provider:
    def __init__(self, credentials):
        self.key = credentials.get("openai")

    def generate(self, prompt, model):
        return "..."
```

Supported provider files include `openai.py` and `ollama.py`.

## Credentials

A provider is only given its own credential. List the stored entry names it
accepts, most canonical first:

```python
CREDENTIAL_KEYS = ("openai", "openai_compat", "OPENAI_API_KEY", "api_key")
```

`astra ask --provider myprovider` resolves the first stored name and builds
`Provider({"openai": "<key>"})`, or `Provider({})` when none is stored — so a
key saved under a legacy name still reaches the provider under the canonical
one. Without `CREDENTIAL_KEYS`, the provider's own name is the only entry read.

## Missing keys

Set `self.configured = bool(<key>)` in `__init__` when the provider cannot work
without a key. `astra ask` then refuses to call it and prints the `creds add`
command to run, instead of returning placeholder output. Providers that need no
key (such as `ollama`) can omit `configured` entirely.
