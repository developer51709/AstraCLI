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
