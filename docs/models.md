# AstraCLI Models

AstraCLI model definitions live in YAML files under `astra/models/`.

## Adding a new model

Create a YAML file with the following structure:

```yaml
name: my-model
provider: ollama
parameters:
  temperature: 0.7
  max_tokens: 2048
```

The CLI loads all YAML model definitions automatically.

`name` is the id you use on the CLI (`astra models`, `--model`, `active_model`).
Add `model:` when the backend expects a different identifier — Ollama tags the
model `llama3.1:8b`, while the CLI id stays `llama3.1-8b`:

```yaml
name: llama3.1-8b
model: llama3.1:8b
provider: ollama
parameters:
  temperature: 0.7
  max_tokens: 2048
```
