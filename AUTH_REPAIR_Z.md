# Auth Repair Z Summary

## Backend
- Cleaned `settings.py` auth settings and integrated Whitenoise for static files.
- Updated middleware and URLs to rely solely on `dj_rest_auth` endpoints.
- Added `collectstatic` call to `make run-backend` and added Whitenoise to requirements.
- Added end‑to‑end auth test covering register → login → profile → logout flow.

## Frontend
- Introduced `AuthService` for JWT handling and refactored `ApiService` and pages to use it.
- Login and registration screens now post to `/api/auth/` endpoints and buttons use theme text styles.
- Added widget test verifying successful login navigates to `TodayPage`.
- Updated `Makefile` frontend recipe to disable VM service publication.

Run `make migrate && make run-backend` then `make run-frontend` to start the app. `collectstatic` runs automatically.
