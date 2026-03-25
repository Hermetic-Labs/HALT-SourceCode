# dev/

> Build, deploy, and quality tooling — prime-author only. Not shipped to users.

## Context

Scripts in this directory support the development lifecycle: downloading dev assets, building platform-specific distributions, uploading to Cloudflare R2, and running lint passes. None of these files are included in production builds. They require environment variables for R2 credentials.

## Files

| File | Purpose | Lines | Usage |
|---|---|---|---|
| `build_and_deploy.py` | Full build pipeline — Electron (Win), standalone (macOS), version bump, zip, R2 upload | ~740 | `python dev/build_and_deploy.py --release` |
| `setup.py` | Post-clone dev setup — downloads AI models + portable Python runtime from R2 | ~200 | `python dev/setup.py` |
| `upload_r2.py` | One-shot upload of HALT-v1.0.zip to R2 (multipart, 100MB chunks) | ~70 | `python dev/upload_r2.py` |
| `white_glove.py` | Master lint orchestrator — 8 passes (Python, JS, HTML, Shell, PS, MD, Data, Hygiene) | ~880 | `python dev/white_glove.py [--strict]` |
| `cloudflare.md` | Documentation for Cloudflare R2/Pages deployment procedures | ~100 | Reference only |
| `.env.example` | Template for required environment variables | ~10 | Copy to `.env` |
| `windows-preflight.ps1` | Windows pre-build checks (Node, Python, runtime validation) | ~80 | CI/manual |

## Subdirectories

| Directory | Purpose |
|---|---|
| `electron-launcher/` | Electron main process + preload scripts for desktop shell |
| `ios-companion/` | Capacitor iOS companion app configuration |
| `macos/` | macOS-specific build scripts and .command launcher |
| `pi5-kiosk-forge/` | Raspberry Pi 5 kiosk mode setup scripts |
| `windows/` | Windows installer resources (NSIS, icons) |

## Environment Variables

| Variable | Used By | Purpose |
|---|---|---|
| `R2_ACCOUNT_ID` | setup.py | Cloudflare account |
| `R2_ACCESS_KEY` | setup.py | R2 API key |
| `R2_SECRET_KEY` | setup.py | R2 API secret |
| `CF_ACCOUNT_ID` | upload_r2.py | Cloudflare account (alt prefix) |
| `CF_R2_ACCESS_KEY` | upload_r2.py | R2 API key (alt prefix) |
| `CF_R2_SECRET_KEY` | upload_r2.py | R2 API secret (alt prefix) |

## Quality

- `white_glove.py` is the codebase lint standard — two tiers:
  - **Default (practical)**: Bugs, unused code, complexity, security only
  - **Strict (`--strict`)**: All Ruff rules including docstrings and style
- Current status: 175 practical lint issues remaining (intentional patterns)
- All dev scripts have module docstrings
