# AGENTS.md — Project Codex Blueprint

## 🚀 Project Name: MoveYourAzz

A full-stack mobile wellness app that uses AI, memes, and group accountability to help coders and creatives get out of their chair and into the world.

This app combines:
- Daily movement tracking
- AI-generated plans and motivation
- Meme-based punishment and badge-based rewards
- Group-based herds and public “donkey shame” accountability

---

## 💻 Stack

| Layer       | Tech                                 |
|-------------|--------------------------------------|
| Backend     | Django 5 + DRF                       |
| Frontend    | Flutter 3                            |
| Database    | Postgres                             |
| AI          | OpenAI (GPT + Whisper), ElevenLabs   |
| Media Gen   | Replicate (images), GIPHY (GIFs)     |
| Tasks       | Celery + Redis (not yet wired)       |
| Storage     | Local for dev, optional S3 prod      |
| Integrations| Twitter/X, Bluesky, Instagram        |

---

## 📦 Django App Modules

| App         | Purpose |
|-------------|---------|
| `core`      | Profiles, streaks, daily lockouts, goals, herds |
| `prompts`   | AI prompts, meme caption generation |
| `movement`  | Workout sessions, logs, mood states |
| `content`   | Meme & image generation, caption APIs |
| `shame`     | Donkey meme builder + herd-feed sharing |

---

## 🔐 Core Mechanics

### 🔒 Lockout System
- Each day the user must log physical activity (via paddle, workout, or streak)
- Failure to meet requirement → donkey meme is posted to shame them

### 🫏 Shame Engine
- Uses OpenAI + GIPHY to generate a meme
- Captioned with roast tone
- Posts to Herd feed and optionally social media
- Triggers badge system, mood updates

### 🛶 Paddle Sessions
- Tracks paddle logs, including GPS + mood
- Optionally uploads photos
- Unlocks rewards and special “Paddle Vibes” content

### 🧠 Voice Journals
- Users can upload voice logs (transcribed via Whisper)
- Summarized and tagged with mood
- Optional playback via ElevenLabs TTS

### 🎯 Goals + Recaps
- Users can set a short daily goal (e.g. journal once)
- Recap page summarizes mood, activity, and AI commentary
- Weekly recap planned for v1.1

---

## 🧱 Notable Models

- `Profile`: user info, streaks, mood, display name
- `DailyLockout`: tracks per-day unlock status
- `MovementSession`: duration, type, success
- `ShamePost`: meme shared due to missed goal
- `PaddleLog`: GPS + paddle session stats
- `GeneratedImage`, `SocialPost`, `VoiceJournal`
- `Badge`, `BadgeShoutout`: unlocked awards
- `Herd`, `HerdPost`: group feed and invites
- `DailyGoal`, `WorkoutLog`: simple movement goals
- `DonkeyChallenge`: AI-generated tasks

---

## 📱 App Screens (Flutter)

1. `TodayPage`: Mood, recap, plan, meme gen, goal
2. `MemeSharePage`: Meme preview, save, share to herd
3. `BadgeGridPage`: Earned badges + filter
4. `HerdFeedPage`: Shared memes, shoutouts
5. `ProfilePage`: Display name, mood, logout
6. `Login/Register`: Auth + token handling
7. `VoiceJournalPage` (TBD): Upload audio, playback

---

## 🧪 Missing or Incomplete

- Celery not wired → all AI runs blocking in production
- `.env` file required but not present — sensitive keys exposed
- ViewSets missing permission classes in `core/views.py`
- GoalSetupPage exists but is never shown
- VoiceJournal not wired into UI
- Meme saving crashes on iOS if permissions not granted

---

## 📝 Codex Guidelines

Codex should:
- Scaffold all models with migrations, serializers, and admin
- Default DRF ViewSets to `IsAuthenticated`
- Avoid `eval()` or raw parsing of AI strings
- Sanitize GPT output to remove encoding artifacts
- Use `.env` variables for all API keys and secrets
- Always wrap OpenAI calls with fallback protection
- Patch `generate_meme`, `generate_plan`, `generate_meal` into Celery once ready
- When adding Flutter screens:
  - Register in `main.dart`
  - Handle token + network errors
  - Use `cleanText()` before display

---

## 📘 Development Notes

- `.venv/` and `db.sqlite3` must never be committed
- `AZZ_MODE` env var may be used to toggle between safe/roast modes
- Feature flag support (badges, voice journal, herds) is encouraged

---

## 🧠 Mission (Why this exists)

Chris built MoveYourAzz to:
- Get healthier
- Rebuild confidence
- Connect with people through humor and honesty
- Launch something real without doomscrolling
- Prove AI isn’t just for chat — it can *move azzes*

---

*This isn’t just a meme app. It’s an accountability engine with attitude.*  
🫏🔥