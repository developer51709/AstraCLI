class Provider:
    def __init__(self, credentials):
        pass

    def generate(self, prompt, model):
        return f"[Ollama local model simulated output for: {prompt}]"
