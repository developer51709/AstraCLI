import os

try:
    import requests
except Exception:
    requests = None

CREDENTIAL_KEYS = ("openai", "openai_compat", "OPENAI_API_KEY", "api_key")


class Provider:
    def __init__(self, credentials):
        self.key = credentials.get("openai")
        self.base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.configured = bool(self.key)

    def generate(self, prompt, model):
        if requests is None:
            return "[astra] error: the 'requests' package is not installed."

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
