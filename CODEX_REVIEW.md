# Code Review – MoveYourAzz

## Repository State
- Django 5 backend with DRF.
- Flutter frontend in `momentum_flutter/`.
- AI integrations for workout/meal plans, memes, voice journals.
- Celery tasks are defined but not actively used.

## Issues
1. **Committed virtual environment** – `.venv/` should be removed from version control.
2. **Incomplete `.env.sample`** – lacks keys such as `ELEVENLABS_API_KEY` and `GIPHY_API_KEY`.
3. **`.env` load path mismatch** – `server/settings.py` expects `backend/.env`.
4. **Celery not installed** – tasks cannot run asynchronously.
5. **Unconnected endpoints**:
   - `/api/content/generate-caption/` unused in Flutter.
   - MovementChallenge/MovementSession APIs unused.
   - `/api/core/share-badge/` unused.
6. **Missing UI features** – no Flutter pages for voice journals or challenge completion.
7. **Duplicated API methods** – `getDailyGoal` vs. `fetchDailyGoal`.
8. **Inconsistent field names** – API returns `type`; model uses `goal_type`.
9. **Limited test coverage** – only core backend tests and a trivial Flutter test.
10. **Hardcoded ElevenLabs voice ID** – should be configurable.

## Suggested Improvements
- Purge `.venv/` from history and ensure `.gitignore` excludes it.
- Place `.env.sample` in `backend/` or update `settings.py` accordingly; include all required keys.
- Add `celery` and broker dependencies to `requirements.txt`; run AI tasks via Celery.
- Build Flutter UI for voice journals, movement challenges, and badge sharing.
- Refactor API client (`ApiService`) to remove duplicates and standardize field names.
- Write tests for remaining apps and more Flutter screens.
- Document setup steps in a root `README.md`.

