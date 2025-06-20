# CODEX_CODE_REVIEW_v2

## Executive Summary
MoveYourAzz now has a cleaner codebase with Celery-powered async tasks and a polished Flutter client. Auth flows were refactored and tests cover voice journals and movement APIs. However, the vision upload endpoint remains public and several legacy tests are still skipped. Linter errors persist and a couple of Flutter routes target missing backend endpoints. Overall security and CI have improved, but more cleanup is required before production.

## Diff vs previous review
| Issue | Status |
|------|--------|
| Committed virtual environment | Fixed |
| Celery not wired | Fixed |
| Mismatched API paths | Fixed |
| Anonymous image identification endpoint open | **Still open** |
| Hard-coded ElevenLabs voice ID | Fixed |
| Skipped legacy tests | **Still open** |
| Broken GitHub Actions workflow | Fixed |
| Unprotected environment configuration | Fixed |
| Numerous flake8 violations | **Still open** |
| Outdated dependencies | Fixed |

## New Findings
### High Severity
- `vision.views.identify_image` allows unauthenticated uploads【F:backend/vision/views.py†L16-L25】.
- Flutter expects `/api/core/upload-voice/` but backend lacks this endpoint【F:frontend/momentum_flutter/lib/services/api_service.dart†L258-L264】.

### Medium Severity
- Several test classes remain skipped【F:backend/core/tests.py†L1-L50】.
- `celery_ping` endpoint is open to everyone【F:backend/core/views.py†L344-L352】.
- `dashboard_feed` assembles Python lists and sorts them, risking N+1 queries【F:backend/core/views.py†L116-L192】.
- `flake8` reports many style errors【5f251e†L1-L10】.

### Low Severity
- Unused endpoints like `generate-caption` remain.
- Flutter build/test skipped when SDK absent.
- Dependencies could not be scanned due to network limits.

## Unconnected Endpoints or Dead Flutter Code
- `/api/core/upload-voice/` and `/api/core/movement/challenges/<id>/complete/` not implemented.
- Unused endpoints in backend: `generate-caption`, `create-goal`, `log-workout`, `update-mood`, `mood-avatar`, some herd management routes.

## Performance & Cost Hotspots
- `dashboard_feed` performs sorting in Python after querying all posts【F:backend/core/views.py†L116-L192】.
- `identify_image_task` fetches OpenAI and Wikipedia for each upload synchronously【F:backend/vision/tasks.py†L8-L33】.

## Dependency Status
`pip list --outdated` could not be executed reliably; consider running locally to verify package versions.

## Open Questions
1. Should the vision identification endpoint require authentication?
2. Are `/api/core/upload-voice/` and challenge completion routes planned or can they be removed from the Flutter client?
3. Should `celery_ping` be restricted to authenticated users?
4. Is lint compliance planned given the current flake8 output?

