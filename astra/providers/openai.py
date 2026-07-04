class Provider:
    def __init__(self, credentials):
        self.key = credentials.get("openai", None)

    def generate(self, prompt, model):
        return f"[OpenAI simulated response to: {prompt}]"
