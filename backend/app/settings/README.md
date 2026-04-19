# Settings

Phase 4 AI settings live in `app/settings/ai.py` and are composed through
`app/core/config.py`.

Environment variables:

- `AI_PROVIDER`: Provider adapter name. The default deterministic provider is local and network-free.
- `AI_MODEL`: Provider model identifier.
- `AI_API_KEY`: Optional provider API key for future non-deterministic adapters.
- `AI_REQUEST_TIMEOUT_SECONDS`: Provider request timeout.
- `AI_MAX_ATTEMPTS`: Total attempts per AI analysis run, capped at 3 for Phase 4.
