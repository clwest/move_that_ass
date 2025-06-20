# CODEX_CODE_REVIEW

## Repository Health

| Category | Score (A–F) | Notes |
|----------|------------|-------|
| Security | C | Several endpoints allow anonymous access (e.g. vision upload), committed `.venv` directory and minimal `.gitignore` increase risk. |
| API Design | C | Flutter routes don't match Django paths and some stale endpoints remain. |
| Async Tasks | D | Celery tasks defined but not consistently used; AI helpers run synchronously. |
| Flutter UX | C | Many pages exist but flows like GoalSetup and VoiceJournal are unreachable. |
| Tests & Coverage | C | Core auth tests pass but many apps have skipped or missing tests. |
| CI/CD | D | GitHub Actions reference non‑existent Makefile targets. |

## Top 10 High-impact / High-risk Issues

1. **Committed virtual environment** – `backend/.venv` is checked into Git which bloats the repo and confuses tooling. `.gitignore` under `backend` only ignores `.env`【F:backend/.gitignore†L1-L1】.
2. **Celery not wired** – AGENTS notes that all AI calls run blocking【F:AGENTS.md†L98-L104】. Tasks like `generate_plan_task` exist but real views call them directly without checking `CELERY_DISABLED`.
3. **Mismatched API paths** – Flutter calls `/api/core/share-badge/` etc. but backend exposes these under `/api/shame/`【F:frontend/momentum_flutter/lib/services/api_service.dart†L233-L254】【F:backend/shame/urls.py†L24-L34】.
4. **Anonymous image identification endpoint** – `vision.views.identify_image` uses `AllowAny` and `csrf_exempt` exposing file upload to anyone【F:backend/vision/views.py†L18-L23】.
5. **Hard‑coded ElevenLabs voice ID** – default voice ID is embedded in code rather than `.env`【F:backend/voice_journals/utils/tts_helpers.py†L4-L9】.
6. **Skipped legacy tests** – multiple test classes marked `@unittest.skip` leaving key features untested (e.g., MovementAPITest)【F:backend/movement/tests.py†L7-L8】.
7. **Broken GitHub Actions workflow** – CI job calls `make test-backend` and `make lint-backend`, targets that do not exist in Makefile【F:.github/workflows/ci.yml†L22-L29】【F:Makefile†L7-L50】.
8. **Unprotected environment configuration** – `.env.sample` exists but `.env` loading path is fixed; secrets may leak if `.env` missing per AGENTS instructions.
9. **Numerous flake8 violations** – running flake8 shows many E501/E402 errors across apps (over 20 issues). Linter failing signals code quality problems.
10. **Outdated dependencies** – `pip list --outdated` shows packages like Celery and simplejwt behind latest versions【644391†L1-L9】.

## Unconnected Endpoints

- Backend routes unused by Flutter: `generate-caption`, `create-goal`, `log-workout`, `update-mood`, `mood-avatar`, all `prompts` endpoints, and herd management endpoints (`create-herd`, `join-herd`, etc.).
- Flutter calls missing in backend: `/api/core/upload-voice/`, `/api/core/movement/challenges/<id>/complete/`, and `/api/core/herd-feed/<id>/like/` do not exist. Several others under `/api/core/` actually live under `/api/shame/` causing 404s.

## Performance / Cost Hotspots

- `dashboard_feed` assembles multiple querysets and sorts in Python which may trigger N+1 queries on large datasets【F:backend/core/views.py†L60-L116】.
- Vision identification task fetches both OpenAI and Wikipedia for each upload, which may be expensive and synchronous【F:backend/vision/tasks.py†L8-L33】.

## Linter / Static-analysis Summary

- `flake8 backend --exclude backend/.venv` reports over 30 E501/E402 errors and unused imports, indicating style inconsistency【9b32e8†L1-L36】.
- Dart analyzer could not run (Flutter SDK missing in CI environment).

## Dependency Review

Outdated packages include Celery 5.3.6 → 5.5.3, simplejwt 5.3.1 → 5.5.0 and openai 1.86 → 1.88【644391†L1-L9】. Consider upgrading and pinning versions.

## Open Questions for the Maintainer

1. Should anonymous image uploads remain open or require authentication?
2. Are movement challenges and herd features actively supported in the mobile app?
3. What is the plan for CI—should it run inside Docker or directly via Makefile?
4. Should voice journal playback be public or restricted to owner only?

## Suggested Next Sprints

- Purge `.venv` and tighten `.gitignore`; standardize environment handling.
- Fix Flutter API paths and unify route design between apps.
- Wire Celery workers and move AI helpers fully asynchronous.
- Expand unit tests for movement, prompts, and voice journals.
- Harden security (permissions, rate limiting, secret management).
- Repair CI workflow to run tests and lints automatically.

