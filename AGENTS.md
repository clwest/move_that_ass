# AGENTS.md — Project Codex Blueprint

## 🚀 Project Name: MoveThatAss

A full-stack wellness app that uses AI, humor, and social shaming to help creators and coders get out of their chair and into the world.

This app combines:
- Movement goals (tracked via sessions, paddle logs, GPS)
- Creative prompts (generate AI art daily)
- Habit incentives and punishments
- Meme-worthy donkey content when goals are missed

---

## 💻 Stack

| Layer | Tech |
|-------|------|
| Backend | Django 5 + DRF |
| Frontend | Flutter 3 |
| Database | Postgres |
| AI | OpenAI or Replicate (for images) |
| Integrations | Twitter/X, Bluesky, Instagram (auto-posting) |
| Optional | Celery, Redis, Firebase, Google Fit/HealthKit |

---

## 📦 Django App Modules

| App | Purpose |
|-----|---------|
| `core` | Users, profiles, streaks, paddleboarding, movement lockouts |
| `prompts` | AI prompt generation + user submissions |
| `movement` | Movement challenges and sessions |
| `content` | Generated images and social post logs |
| `shame` | Donkey meme generation and public roast automation |

---

## 🔐 Core Mechanics

### Lockout System
- User must complete X minutes of movement per day
- If not completed: creative tools are locked, and shame post is triggered

### Shame Engine
- AI generates “shameful donkey” image + caption
- Auto-posts to Twitter, Bluesky, Instagram
- Users can review shame history in-app

### Paddleboarding Bonus
- Logs paddle sessions with location, mood, optional photo
- Unlocks reward screens and badge incentives
- Special “Paddle Vibes” content released post-session

---

## 🧱 Models in Core App

- `Profile`: user info, streaks, daily stats
- `DailyLockout`: tracks required movement + unlock status
- `ShamePost`: stores donkey memes + public post logs
- `PaddleLog`: records paddle sessions
- `Prompt`, `PromptResponse`: creative flows
- `GeneratedImage`, `SocialPost`: AI outputs + shares

---

## 📱 App Screens (Flutter)

1. **Dashboard**: today’s prompt + lockout status
2. **Move Tracker**: walk or paddle log
3. **Image Gen**: creative tool (locked until unlocked)
4. **Social Share**: post preview + auto-post
5. **Shame Feed**: view past donkey posts (and cry)

---

## 🎯 Mission

Chris is building this app to:
- Lose 15+ lbs
- Gain confidence
- Paddle more often (especially around someone 👀)
- Build a shareable brand without doomscrolling
- Launch something complete — fast

---

## ✅ Codex Guidelines

Codex should:
- Scaffold all models with migrations + serializers + admin config
- Wire up REST APIs per app (`api/core/`, `api/prompts/`, etc.)
- Avoid hardcoding credentials or API tokens
- Prioritize health → humor → creativity → share flow
- Build toward MVP readiness for TestFlight / Play Store

---

*This app doesn’t just move pixels. It moves azzes.* 🫏🔥
