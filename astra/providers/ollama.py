import os

from astra.core.exceptions import ProviderError

try:
    import requests
except Exception:
    requests = None


class Provider:
    def __init__(self, credentials):
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").strip()
        if "://" not in host:
            host = f"http://{host}"
        self.base = host.rstrip("/")

    def generate(self, prompt, model):
        if requests is None:
            raise ProviderError("the 'requests' package is not installed")

        model_name = (model.get("model") or model.get("name")) if isinstance(model, dict) else str(model)
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }

        options = {}
        if isinstance(model, dict):
            params = model.get("parameters", {})
            if "temperature" in params:
                options["temperature"] = params["temperature"]
            if "max_tokens" in params:
                options["num_predict"] = params["max_tokens"]
        if options:
            payload["options"] = options

        url = f"{self.base}/api/chat"
        try:
            resp = requests.post(url, json=payload, timeout=60)
        except requests.exceptions.ConnectionError as exc:
            raise ProviderError(
                f"cannot reach Ollama at {self.base}; is it running? "
                f"(set OLLAMA_HOST if it listens elsewhere)"
            ) from exc
        except Exception as exc:
            raise ProviderError(f"ollama request failed: {exc}") from exc

        try:
            data = resp.json()
        except ValueError:
            data = {}

        if resp.status_code >= 400:
            detail = data.get("error") if isinstance(data, dict) else None
            raise ProviderError(
                f"ollama request failed ({resp.status_code}) at {self.base}: "
                f"{detail or resp.reason}"
            )

        message = data.get("message") if isinstance(data, dict) else None
        if isinstance(message, dict) and "content" in message:
            return message["content"]
        if isinstance(data, dict) and "response" in data:
            return data["response"]

        raise ProviderError(f"ollama response contained no message: {data}")
