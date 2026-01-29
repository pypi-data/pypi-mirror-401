import json
import urllib.request


DEFAULT_BASE_URL = "https://prompttube.ai"


class PromptTube:
    def __init__(self, api_key, base_url=DEFAULT_BASE_URL):
        if not api_key:
            raise ValueError("PromptTube API key is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def _request(self, method, path, body=None):
        url = f"{self.base_url}{path}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req) as res:
            payload = res.read().decode("utf-8")
            return json.loads(payload) if payload else None

    def list_prompts(self, limit=20, cursor=None):
        params = {"limit": str(limit)}
        if cursor:
            params["cursor"] = cursor
        query = "&".join([f"{k}={v}" for k, v in params.items()])
        return self._request("GET", f"/api/v0/prompts?{query}")

    def get_prompt(self, prompt_id):
        if not prompt_id:
            raise ValueError("prompt_id is required")
        return self._request("GET", f"/api/v0/prompts/{prompt_id}")

    def run(self, messages, tier=None, provider=None, model=None):
        if not messages:
            raise ValueError("messages are required")
        return self._request(
            "POST",
            "/api/v0/run",
            {
                "messages": messages,
                "tier": tier,
                "provider": provider,
                "model": model,
            },
        )

    def create_summary(self, chat_id=None, text=None, intent=None, reusable_prompt=None):
        if not chat_id and not text:
            raise ValueError("chat_id or text is required")
        return self._request(
            "POST",
            "/api/v0/summaries",
            {
                "chatId": chat_id,
                "text": text,
                "intent": intent,
                "reusable_prompt": reusable_prompt,
            },
        )
