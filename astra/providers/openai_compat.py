import os

try:
    import requests
except Exception:
    requests = None


class Provider:
    def __init__(self, credentials):
        # credentials can be a dict with provider keys
        self.key = None
        if isinstance(credentials, dict):
            self.key = credentials.get("openai") or credentials.get("OPENAI_API_KEY") or credentials.get("api_key")
        self.base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")

    def generate(self, prompt, model):
        # If requests isn't available or no API key provided, fall back to simulated output
        if requests is None or not self.key:
            return f"[OpenAI-compatible provider simulated response for: {prompt}]"

        url = f"{self.base}/chat/completions"
        model_name = model.get("name") if isinstance(model, dict) else str(model)
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
        }
        # include optional parameters
        if isinstance(model, dict):
            params = model.get("parameters", {})
            payload.update({k: v for k, v in params.items() if k in ("temperature", "max_tokens")})

        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            if "choices" in data and data["choices"]:
                choice = data["choices"][0]
                if isinstance(choice.get("message"), dict):
                    return choice["message"].get("content", "")
                return choice.get("text", "")
            return str(data)
        except Exception as exc:
            return f"[OpenAI-compatible provider error: {exc}]"
