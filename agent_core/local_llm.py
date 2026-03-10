from typing import Optional, Dict
from dataclasses import dataclass
from enum import Enum
import os
import time
import hashlib


class LocalBackend(Enum):
    OLLAMA = "ollama"


@dataclass
class TinyLlamaConfig:
    """
    Configuration optimized for TinyLlama.
    """

    backend: LocalBackend = LocalBackend.OLLAMA
    model_name: str = "tinyllama"

    temperature: float = 0.7
    max_tokens: int = 256
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1

    timeout: int = 60

    enable_cache: bool = True
    cache_size: int = 500

    # LOCAL OLLAMA URL (FIXED)
    ollama_url: str = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434"
    )


class ResponseCache:

    def __init__(self, max_size: int = 500):
        self._cache: Dict[str, str] = {}
        self._max_size = max_size

    def get(self, key: str):
        return self._cache.get(key)

    def set(self, key: str, value: str):

        if len(self._cache) >= self._max_size:
            first_key = next(iter(self._cache))
            del self._cache[first_key]

        self._cache[key] = value

    def clear(self):
        self._cache.clear()


class TinyLlamaClient:

    def __init__(self, config: Optional[TinyLlamaConfig] = None):

        self.config = config or TinyLlamaConfig()
        self._cache = ResponseCache(self.config.cache_size)

        self._stats = {
            "total_requests": 0,
            "success": 0,
            "failures": 0,
            "latency": 0
        }

        self._init_backend()

    # -------------------------
    # Backend initialization
    # -------------------------

    def _init_backend(self):

        if self.config.backend == LocalBackend.OLLAMA:
            self._init_ollama()

    def _init_ollama(self):

        try:
            import requests

            url = f"{self.config.ollama_url}/api/tags"

            r = requests.get(url, timeout=5)

            if r.status_code == 200:
                print(f"✓ Connected to Ollama at {self.config.ollama_url}")
            else:
                print(f"⚠ Ollama returned {r.status_code}")

        except Exception as e:

            print("⚠ Could not reach Ollama server")
            print("Make sure Ollama is running:")
            print("   ollama serve")
            print("Error:", e)

    # -------------------------
    # Main generation API
    # -------------------------

    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:

        self._stats["total_requests"] += 1

        if not prompt.strip():
            return "[Error: Empty prompt]"

        cache_key = self._cache_key(prompt)

        cached = self._cache.get(cache_key)
        if cached:
            return cached

        try:

            start = time.time()

            response = self._call_ollama(
                prompt,
                temperature or self.config.temperature,
                max_tokens or self.config.max_tokens
            )

            self._stats["latency"] += time.time() - start
            self._stats["success"] += 1

            self._cache.set(cache_key, response)

            return response

        except Exception as e:

            self._stats["failures"] += 1
            return f"[Error: {str(e)}]"

    # -------------------------
    # Ollama call
    # -------------------------

    def _call_ollama(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:

        import requests

        payload = {
            "model": self.config.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "top_p": self.config.top_p,
                "top_k": self.config.top_k,
                "repeat_penalty": self.config.repeat_penalty
            }
        }

        r = requests.post(
            f"{self.config.ollama_url}/api/generate",
            json=payload,
            timeout=self.config.timeout
        )

        if r.status_code != 200:
            raise RuntimeError(
                f"Ollama API error {r.status_code}: {r.text}"
            )

        data = r.json()

        return data.get("response", "").strip()

    # -------------------------
    # Helpers
    # -------------------------

    def _cache_key(self, prompt: str) -> str:
        return hashlib.md5(prompt.encode()).hexdigest()

    @property
    def stats(self):
        return self._stats

    def clear_cache(self):
        self._cache.clear()


# -------------------------
# Global client
# -------------------------

_client: Optional[TinyLlamaClient] = None


def get_client() -> TinyLlamaClient:

    global _client

    if _client is None:
        _client = TinyLlamaClient()

    return _client


def ask_llm(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 256
):

    client = get_client()

    return client.generate(
        prompt,
        temperature,
        max_tokens
    )
