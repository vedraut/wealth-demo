"""
Unified LLM client with Ollama primary and Kimi K2.6 fallback via OpenClaw.
"""

import os
import json
import requests
from typing import Optional

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OPENCLAW_URL = os.getenv("OPENCLAW_URL", "http://localhost:18789")


class LLMClient:
    """Client that tries Ollama first, falls back to Kimi K2.6 via OpenClaw."""

    def __init__(self, ollama_model: str = "qwen3.5:9b"):
        self.ollama_model = ollama_model
        self.ollama_available = self._check_ollama()

    def _check_ollama(self) -> bool:
        """Check if Ollama is running."""
        try:
            resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
            return resp.status_code == 200
        except Exception:
            return False

    def _call_ollama(self, prompt: str, system: Optional[str] = None) -> str:
        """Call Ollama for inference."""
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system

        resp = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json()["response"]

    def _call_kimi(self, prompt: str, system: Optional[str] = None) -> str:
        """Fallback: Call Kimi K2.6 via OpenClaw API."""
        # OpenClaw API format for agent turn
        payload = {
            "message": prompt,
            "model": "kimi",
        }
        if system:
            payload["system"] = system

        # Use OpenClaw's session API or direct LLM endpoint
        # This is a simplified version - adjust based on your OpenClaw setup
        headers = {"Content-Type": "application/json"}
        resp = requests.post(
            f"{OPENCLAW_URL}/v1/chat/completions",
            json={
                "model": "moonshot/kimi-k2.6",
                "messages": [
                    {"role": "system", "content": system or "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            },
            headers=headers,
            timeout=120
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """Generate text using Ollama (primary) or Kimi (fallback)."""
        if self.ollama_available:
            try:
                return self._call_ollama(prompt, system)
            except Exception as e:
                print(f"⚠️ Ollama failed: {e}. Falling back to Kimi K2.6...")
                return self._call_kimi(prompt, system)
        else:
            print("⚠️ Ollama not available. Using Kimi K2.6 fallback.")
            return self._call_kimi(prompt, system)


# Singleton instance
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create the singleton LLM client."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
