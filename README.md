# AstraCLI  
AstraCLI is a modular, extensible AI command‑line assistant that supports **local models**, **external API providers**, **plugin tools**, and **automatic self‑updates**.  
It is designed for developers who want a fast, offline‑friendly, customizable AI workflow directly from the terminal.

---

## ✨ Features

### 🔹 Unified AI Interface  
Use one CLI tool to interact with:
- Local models (Ollama, llama.cpp, GPT4All)
- External APIs (OpenAI, Groq, Gemini, Anthropic, Mistral)

### 🔹 Modular Provider System  
Providers live in `astra/providers/` and auto‑load at runtime.  
Add new providers by dropping in a Python file.

### 🔹 Modular Model System  
Models are defined in YAML configs under `astra/models/`.  
Supports local GGUF models and remote API models.

### 🔹 Secure Credential Manager  
API keys are stored locally in `~/.astra/credentials.json` with optional encryption.

### 🔹 Plugin Architecture  
Drop tools into `astra/plugins/` to extend AstraCLI:
- Code refactoring
- Bot command generation
- Log analysis
- Prompt testing

### 🔹 Self-Updating Engine  
Run:
```
astra update
```
AstraCLI fetches the latest version, modules, and configs from GitHub automatically.

### 🔹 Offline-Friendly  
Local models and rule-based tools work without internet.

---

## 📁 Repository Structure

```
astra-cli/
│
├── astra/
│   ├── core/
│   ├── providers/
│   ├── models/
│   ├── plugins/
│   ├── utils/
│   └── data/
│
├── tests/
├── scripts/
├── docs/
├── examples/
│
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
└── setup.cfg
```

---

## 🚀 Installation

Clone the repository:
```bash
git clone https://github.com/developer51709/AstraCLI
cd AstraCLI
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run AstraCLI:
```bash
python -m astra
```

---

## 🧠 Usage Examples

### Ask AI
```bash
astra ask "Explain this Python error."
```

### Generate a Discord bot command
```bash
astra gen command ban
```

### Refactor code
```bash
astra refactor bot.py
```

### Analyze logs
```bash
astra analyze logs/latest.log
```

### Update AstraCLI
```bash
astra update
```

---

## 🔌 Adding Providers

Create a new file in:

```
astra/providers/myprovider.py
```

Implement:
```python
class Provider:
    def __init__(self, credentials):
        ...

    def generate(self, prompt, model):
        ...
```

AstraCLI will auto‑detect it.

---

## 🧩 Adding Models

Add a YAML file in:

```
astra/models/my-model.yaml
```

Example:
```yaml
name: llama3.1-8b
provider: ollama
parameters:
  temperature: 0.7
  max_tokens: 2048
```

---

## 🧩 Adding Plugins

Drop a Python file into:

```
astra/plugins/
```

Example:
```python
def run(context):
    # context contains prompt, model, provider, etc.
    return "Plugin output"
```

---

## 🤝 Contributing

Pull requests are welcome!  
Please follow the commit template and issue templates included in `.github/`.

---

## 📜 License

MIT License.  
See `LICENSE` for details.
