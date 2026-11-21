import os

from astra.core.exceptions import ProviderError

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
            raise ProviderError("the 'requests' package is not installed")

        url = f"{self.base}/chat/completions"
        model_name = (model.get("model") or model.get("name")) if isinstance(model, dict) else str(model)
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
        except Exception as exc:
            raise ProviderError(f"openai request failed: {exc}") from exc

        choices = data.get("choices") if isinstance(data, dict) else None
        if not choices:
            raise ProviderError(f"openai response contained no choices: {data}")

        choice = choices[0]
        if isinstance(choice.get("message"), dict):
            return choice["message"].get("content", "")
        return choice.get("text", "")
