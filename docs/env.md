# Environment & Secrets

This project loads configuration from environment variables using **pydantic-settings** and a local `.env` file.

## Files
- `.env.example`: Template that lists all required variables with safe placeholders. **Committed**.
- `.env`: Actual local values. **Not committed** (listed in `.gitignore`).

## Variables
- `APP_ENV` — One of `development`, `staging`, `production`. Controls run-mode behavior.
- `LOG_LEVEL` — One of `DEBUG`, `INFO`, `WARNING`, `ERROR`. Controls logging verbosity.
- `EXTERNAL_API_KEY` — Placeholder for third-party APIs this server might call.

## How loading works
1. The app defines a `Settings` class (see `app/config.py`) using `pydantic-settings`.
2. It points to `.env`, so values are automatically loaded at startup.
3. Precedence (highest to lowest):
   - Real environment variables (shell)
   - `.env` file
   - Defaults defined in code

## Quick start
1. Copy `.env.example` → `.env`
2. Fill real values in `.env`
3. Run:
   ```bash
   uv run python -c "from app.config import settings; print(settings.model_dump())"
