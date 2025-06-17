# LAUNCH_PLAN.md — MoveYourAzz 🚀

## 🧠 What is MoveYourAzz?

A full-stack AI-powered mobile app that uses memes, donkey roasts, and group accountability to get users moving — physically, emotionally, and socially.

Combines:
- AI-generated shame memes 🫏
- Movement tracking & voice journaling
- Herd-based motivation & badge-based rewards
- Recaps, mood tracking, and savage encouragement

Built in public as part of the $100k AI Challenge.

---

## 📦 Deployment Targets

| Target | Status |
|--------|--------|
| ✅ Android Store build     | Almost ready |
| ✅ iOS Store build         | In testing (meme save fix pending) |
| 🔒 API production deploy   | In progress (settings cleanup needed) |
| 🧪 Beta test group         | Set — optional TestFlight or Firebase |
| 📣 Launch promo channels  | Instagram, TikTok, Bluesky, X |

---

## 🚀 Current Phase: Z5 (Codex Audit & Cleanup)

Codex has completed a full system audit:
- ✅ Text cleanup (smart quote artifacts, meme caption issues)
- ✅ Meme generator routing
- 🛠 Remaining items: 
  - Secure `.env` handling
  - Remove `.venv/`, `db.sqlite3` from repo
  - Lock DRF endpoints with permissions
  - Wire `GoalSetupPage`
  - Refactor async AI helpers under Celery
  - Fix meme-save iOS crash (photo permissions)

---

## 🧩 Launch-Blocking Issues (Prioritized)

| Priority | Issue |
|----------|-------|
| 🔥 High  | DRF viewsets unauthenticated by default |
| 🔥 High  | Hardcoded secrets in settings.py |
| ⚠️ Med   | App startup slow due to chained API calls |
| ⚠️ Med   | Welcome dialog reappears on every launch |
| ✅ Fixed | Meme FAB routing to MemeSharePage |
| ⚠️ Med   | GoalSetupPage unreachable from _determineHome |
| ⚠️ Med   | VoiceJournal flow unlinked in UI |
| ⚠️ Med   | No async queue for long GPT calls |
| ⚠️ Med   | Flutter `ApiService.baseUrl` hardcoded |
| ⚠️ Med   | Meme save-to-device crashes on iOS |
| ⚠️ Low   | Missing Celery config & background tasks |

---

## 🗂 Roadmap After Launch (v1.1+)

| Feature | Description |
|---------|-------------|
| 📅 Google Calendar | Sync workouts, schedule donkey tasks |
| 📣 Notification Engine | “Get up and move your azz” alerts |
| 🔊 Voice Journal Playback | TTS summaries via ElevenLabs |
| 🎭 Donkey Tone Packs | Switch between Savage, Zen, Wholesome |
| 🛍 Azz Merch Unlocks | Buyable rewards gated by badge tiers |
| 📈 Weekly Recap | Donkey writes your “Azz Report” |
| 🎟 Invite Rewards | Unlock meme modes by inviting friends |

---

## 📝 Pre-Submission To-Dos

| Task | Status |
|------|--------|
| [ ] Replace all uses of `eval()` |
| [ ] Confirm all OpenAI client fallbacks work offline |
| [ ] Ensure `.env.sample` exists |
| [ ] Add `.flutter-plugins`, `.venv/`, `db.sqlite3` to `.gitignore` |
| [ ] Write docstrings for all views and models |
| [ ] Ensure all `Text()` uses `cleanText()` |
| [ ] Add toast on meme save success/failure |
| [ ] Final pass on App Store screenshots and icon |

---

## 🧾 Store Metadata (Draft)

| Field | Copy |
|-------|------|
| **App Name** | MoveYourAzz |
| **Subtitle** | Get off your azz, one meme at a time |
| **Keywords** | accountability, meme coach, AI fitness, donkey shame, productivity, workout |
| **Short Description** | Stop doomscrolling. Start azz-moving. A donkey-powered assistant that shames you into better habits. |
| **Long Description** |  
MoveYourAzz is your roast-powered AI accountability buddy.  
Log workouts, set goals, share memes, and let the donkey drag you out of bed with a gif and a growl.  
Built for creators, coders, and couch potatoes. Earn badges. Join a herd. Become the azz legend you were born to be.  
Now stop scrolling and start sweating. The donkey is watching.

---

## 📣 Launch Channels

| Channel | Action |
|---------|--------|
| TikTok  | Showcasing donkey recap animation & meme reaction |
| X       | Meme thread series of “Shame of the Day” |
| Bluesky | Devlog + AI ethics posts |
| Instagram | Story templates, “daily roast,” user badges |
| Product Hunt | Submit launch under AI + Fitness |
| YouTube Shorts | Donkey TTS + meme skits + launch devlog |

---

*The donkey is ready. Are you? 🫏🔥*