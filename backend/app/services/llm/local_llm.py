"""
Local text generation -- Qwen2.5-1.5B-Instruct, quantized to GGUF (Q4_K_M),
run entirely in-process via llama-cpp-python. No network call, no API key,
ever. Chosen for the speed/knowledge tradeoff the user asked for: small enough
to answer in a few seconds on CPU, while still being a real instruction-tuned
model (not a toy) for DSA/system-design explanations.

This model is used ONLY for phrasing/explaining facts that were already
computed deterministically elsewhere (the diagnosis engine's evidence list,
the interview stage machine's structure) -- never as the source of truth for
correctness, scoring, or test results. See callers for the grounding prompts.
"""
from __future__ import annotations

import os
import threading
from functools import lru_cache
from pathlib import Path

MODEL_PATH = Path(os.environ.get("ALGOMIND_LLM_MODEL_PATH", Path(__file__).resolve().parents[3] / "models" / "model.gguf"))
_lock = threading.Lock()


class LocalLLMUnavailable(Exception):
    pass


@lru_cache(maxsize=1)
def _get_model():
    if not MODEL_PATH.exists():
        raise LocalLLMUnavailable(
            f"Local model not found at {MODEL_PATH}. Run backend/app/services/llm/download_model.py first."
        )
    from llama_cpp import Llama

    return Llama(
        model_path=str(MODEL_PATH),
        n_ctx=2048,
        n_threads=max(1, (os.cpu_count() or 4) - 1),
        verbose=False,
    )


def generate(system_prompt: str, user_prompt: str, max_tokens: int = 220, temperature: float = 0.3) -> str:
    """Thread-safe: llama.cpp's context object isn't safe for concurrent calls,
    so we serialize generations behind a lock rather than pretend we can run
    multiple in parallel -- a request will queue briefly instead of corrupting output."""
    model = _get_model()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    with _lock:
        result = model.create_chat_completion(
            messages=messages, max_tokens=max_tokens, temperature=temperature,
        )
    return result["choices"][0]["message"]["content"].strip()


def is_available() -> bool:
    return MODEL_PATH.exists()
