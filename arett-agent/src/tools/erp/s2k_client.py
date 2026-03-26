import os
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


class S2KClient:
    """Base S2K REST client with auth, timeout, and retries."""

    def __init__(self):
        base_url = os.getenv('S2K_BASE_URL', '').strip()
        api_key = os.getenv('S2K_API_KEY', '').strip()
        self.client = httpx.Client(
            base_url=base_url,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            timeout=30.0,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def get(self, path: str, params: dict | None = None) -> dict:
        resp = self.client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def post(self, path: str, body: dict) -> dict:
        resp = self.client.post(path, json=body)
        resp.raise_for_status()
        return resp.json()
