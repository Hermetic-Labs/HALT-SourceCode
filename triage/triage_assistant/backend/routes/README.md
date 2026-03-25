# triage/triage_assistant/backend/routes/

> AI-only route modules for the standalone Triage Assistant.

## Context

These are the route modules for the triage-only backend. They mirror the AI routes from `api/routes/` but are self-contained — they resolve `MODELS_DIR` independently from the `EVE_MODELS_DIR` environment variable rather than importing from a shared `config.py`.

## Files

| File | Purpose | Lines | Endpoints |
|---|---|---|---|
| `health.py` | Model readiness probe | ~23 | `GET /health` |
| `inference.py` | MedGemma LLM — SSE streaming chat | ~119 | `POST /inference/stream`, `GET /models` |
| `tts.py` | Kokoro ONNX TTS — REST + WebSocket | ~182 | `POST /tts/synthesize`, `WS /tts/ws`, `GET /tts/voices`, `GET /tts/health` |
| `stt.py` | Faster-Whisper speech-to-text | ~66 | `POST /stt/listen`, `GET /stt/health` |
| `image.py` | SD-Turbo GGUF image generation — grayscale medical diagrams | ~106 | `POST /image/generate`, `GET /image/health` |
| `__init__.py` | Package marker | 0 | — |

## Key Differences from `api/routes/`

| Aspect | `api/routes/` | This directory |
|---|---|---|
| Model path | Via shared `config.py` | Self-resolved from `EVE_MODELS_DIR` env |
| TTS | Multilingual voice routing + Japanese romaji | Simpler — no `_pick_voice()`, no fugashi |
| Inference | Async lock queue with position feedback | Direct synchronous — no queue |
| Image | Not available | ✅ SD-Turbo GGUF for medical diagrams |
| Thread warmup | Lazy-load on first request | Pre-load at import time via `threading.Thread` |

## Endpoint Index

| Pattern | File |
|---|---|
| `/health` | `health.py` |
| `/inference/*`, `/models` | `inference.py` |
| `/tts/*` | `tts.py` |
| `/stt/*` | `stt.py` |
| `/image/*` | `image.py` |
