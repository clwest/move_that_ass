# MoveYourAzz Merge Plan

## Keep
- Django apps: `core`, `content`, `movement`, `prompts`
- Core models such as `Profile`, `DailyLockout`, `ShamePost`, `VoiceJournal`, `WorkoutLog`, `Herd`, `Badge` and related serializers.
- Celery configuration (`backend/server/celery.py`) and task definitions.

## Refactor / Risky Areas
- All API views currently default to `AllowAny`; switch to `IsAuthenticated`.
- AI helper functions (`plan_engine`, `meal_engine`, `meme_engine`, `voice_helpers`) run synchronously—convert to Celery tasks.
- Hard-coded secrets and voice IDs; replace with environment variables loaded from `.env`.
- README merge conflict and missing project-wide setup instructions.
- Duplicate or unused endpoints (`generate-caption`, `MovementChallenge` views) should be trimmed or integrated.
- Flutter API client has overlapping methods and a hardcoded `baseUrl` fallback.
- Voice journal and challenge completion flows are only partially implemented.

## Merge Targets
- Consolidate shame-related logic into a new `shame` app.
- Extract voice journal logic to its own `voice_journals` app for clarity.
- Combine repeated goal endpoints (`daily_goal_view` vs `create_goal`) where feasible.
- For Flutter, merge duplicated navigation logic and centralize service calls in `ApiService`.

## Proposed Folder Structure
/backend
  /core/
  /movement/
  /content/
  /shame/
  /prompts/
  /voice_journals/
  celery.py

/frontend
  /lib/pages/
    TodayPage.dart
    MemeSharePage.dart
    VoiceJournalPage.dart
    ChallengeResultPage.dart
  /lib/services/
    ApiService.dart
    AuthService.dart
  /lib/widgets/
  /lib/constants/
  main.dart

