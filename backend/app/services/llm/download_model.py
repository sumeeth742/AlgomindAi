"""
One-time download of the local LLM weights (~1.1GB). Run with:
    python -m app.services.llm.download_model

Downloads Qwen2.5-1.5B-Instruct, Q4_K_M GGUF quantization -- a public,
Apache-2.0-licensed model, no Hugging Face token required.
"""
import urllib.request
from pathlib import Path

MODEL_URL = "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf"
DEST = Path(__file__).resolve().parents[3] / "models" / "model.gguf"


def main():
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.exists():
        print(f"Already present: {DEST} ({DEST.stat().st_size / 1e6:.0f} MB)")
        return
    print(f"Downloading {MODEL_URL} -> {DEST}")
    urllib.request.urlretrieve(MODEL_URL, DEST)
    print(f"Done: {DEST.stat().st_size / 1e6:.0f} MB")


if __name__ == "__main__":
    main()
