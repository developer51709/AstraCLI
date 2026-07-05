# AstraCLI Plugins

Plugins extend AstraCLI with custom tools.

## Adding a new plugin

Create a Python file in `astra/plugins/` with a `run(context)` function:

```python
def run(context):
    return "Plugin output"
```

Use `astra plugins` to list plugins and `astra plugins run <plugin>` to execute one.
