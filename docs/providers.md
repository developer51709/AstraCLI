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
