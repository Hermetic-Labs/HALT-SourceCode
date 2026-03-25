# triage/triage_assistant/backend/

> Standalone AI runtime for the Triage Assistant — a lighter deployment that ships without the full patient management or mesh networking stack.

## Context

This is a **separate FastAPI application** from `api/`. It serves the standalone "Triage Assistant" which bundles only the AI inference capabilities (MedGemma, Kokoro TTS, Whisper STT, SD-Turbo image generation) and a static HTML frontend. No patient records, no mesh, no wards. Think of it as the embedded AI engine.

The main HALT API (`api/`) and this triage backend share overlapping route implementations (TTS, STT, inference) but are maintained independently — this backend has its own `requirements.txt`, its own `main.py`, and self-contained model path resolution.

## Files

| File | Purpose | Lines | Key Difference from `api/` |
|---|---|---|---|
| `main.py` | FastAPI entrypoint — mounts frontend, warms TTS in background thread | ~58 | No CORS complexity, no lifespan hooks, simpler startup |
| `requirements.txt` | Slimmer dependency list — AI libs only | ~10 | No cryptography, no qrcode, no mesh deps |
| `routes/` | Route modules — see `routes/README.md` | — | Adds `image.py` (SD-Turbo), no mesh/patients/inventory |

## Architecture

```
main.py ──imports──→ routes/health.py
                  ──→ routes/inference.py
                  ──→ routes/tts.py       (prefix /tts)
                  ──→ routes/stt.py       (prefix /stt)
                  ──→ routes/image.py     (prefix /image)
                  ──→ static frontend (../frontend/)

TRIAGE_ROOT env var → parent of backend/
  ├── backend/     ← you are here
  ├── frontend/    ← static HTML
  └── models/      ← AI models
```

## Relationship to `api/`

| Feature | `api/` (Full HALT) | This backend (Triage Assistant) |
|---|---|---|
| AI Inference | ✅ MedGemma | ✅ MedGemma |
| TTS | ✅ Kokoro (multilingual) | ✅ Kokoro (simpler, no language routing) |
| STT | ✅ Faster-Whisper | ✅ Faster-Whisper |
| Image Gen | ❌ | ✅ SD-Turbo GGUF |
| Patient Records | ✅ Encrypted JSON | ❌ |
| Mesh Networking | ✅ WebSocket + QR | ❌ |
| Inventory | ✅ | ❌ |
| Translation | ✅ NLLB-200 | ❌ |
| Ward Management | ✅ | ❌ |
