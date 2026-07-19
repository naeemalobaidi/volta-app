# CLAUDE CODE BRIEF — VOLTA MVP Build (v1)

> Paste this entire file into Claude Code as the kickoff prompt. It is self-contained.
> You are the ONLY writer to the code repo. Build exactly to this spec. The doctrine is the law.

---

## 0. What you're building

**VOLTA** — a mobile-first longevity PWA. One number every morning (the Battery), one action per day, weekly fat-vs-muscle truth, and a long-term Capacity score. Think fade.markets architecture discipline applied to health: **server-authoritative, one generated frontend file, zero frameworks.**

This brief covers the **MVP only**: auth → survey → North Star reveal → daily Battery home → 60-second checklist → weekly report. Everything else (Capacity, Ledger, Twin, bloodwork, course player) is stubbed behind locked screens for Phase 2.

---

## 1. Architecture (match the Fade pattern)

- **Frontend = ONE generated file.** `preview/app_build.py` (Python, raw-string template) emits `preview/app.html`. Vanilla JS + CSS variables, dark theme default + light theme, mobile viewport first (~420px). No React, no npm. Edit ONLY the build script, never the generated html. Inline everything (fonts base64 if needed).
- **Backend = FastAPI** (`backend/app/`) with clean module map:
  - `auth/` — bcrypt + JWT, rolling session token, re-validate on foreground
  - `scoring/` — battery.py, phases.py, checklist.py (ALL scores computed server-side; client only displays)
  - `data/` — apple_health.py (ingestion stub for MVP), oura.py (stub), scale.py (manual entry for MVP)
  - `db/` — SQLAlchemy Core; SQLite local / Postgres on Render
  - `ai/` — coach.py (Phase 2 stub — one endpoint returning the "one action" from rules engine, NOT an LLM for MVP)
- **Server is the source of truth.** Battery, phase logic, verdicts — computed server-side. The client NEVER receives the scoring weights. Proprietary logic never ships to the client.
- **Every external fetch:** cache + TTL + lock + last-good fallback from day one.
- **Deploy:** single repo for now — Render (backend) + the built html served statically. Keep a `window.VOLTA_API` pointer line that gets re-injected on every build (the Fade lesson: a dropped API pointer = silent offline mode).

## 2. The design system (match the mockups exactly)

Reference mockups: `~/healthapp/app-screens.html` (22 screens) and `~/healthapp/preview.html`. **Match these exactly** — dark slate aesthetic:
```
--bg:#06070a; --panel:#0d0f14; --panel2:#11141b; --line:#1c212c;
--txt:#e8ecf3; --dim:#8b93a5; --faint:#5a6274;
--green:#3ddc84; --amber:#ffb340; --red:#ff5a5a; --cyan:#41d6e8; --violet:#9b7bff;
```
Cards: 16–18px radius, 1px --line border, --panel2 bg. Phone-first. Numbers use tabular-nums. Bottom nav: TODAY · PATH · BODY · SCORE (BODY/SCORE locked in MVP with 🔒 teaser).

## 3. The screens to build (MVP)

### 3.1 Auth
Email + password, bcrypt, JWT rolling token. Clean, dark, minimal. No social login for MVP.

### 3.2 The Survey (4 steps — see mockup Part 1)
1. **The Outcome:** longevity / lean / energy / bloodwork (single select)
2. **The Starting Point:** age, height, weight, BF estimate (or "measure it for me"), + the neutral question: "Are you working with a doctor on any medical weight-management plan?" yes/no. Store but never act on medically.
3. **The Baseline:** training days/wk, drinks/wk, diet honesty, sleep hours (tap selectors)
4. **The Commitment:** "Will you track honestly every day?" → Build My Plan.
Server derives: starting phase (always Phase 1), calorie target (Mifflin-St Jeor × activity, slight deficit NOT applied in Phase 1), protein target (1g/lb goal BW), North Star date estimate.

### 3.3 The North Star Reveal (mockup Part 2, screen N1)
"YOUR NORTH STAR: 12%" — slider from current BF to 10–12% zone, the 4 why-bullets (visceral fat clears, insulin resets, hormones normalize, every longevity marker moves), "Not a crash diet. A whole-foods rebuild." CTA: Accept the Target →

### 3.4 TODAY — the Battery home (mockup Part 3, screen D1)
- Ring (SVG, dasharray), number 0–100, level label (LOW/GOOD/CHARGED), one-line recommendation ("Train moderate today")
- The waterfall: every factor with signed points (+14 deep sleep, −9 drinks...). **Every point explainable — this is the product.**
- TODAY'S ONE ACTION card (rules engine output, see §5)
- Tomorrow's projected battery (updates as checklist items complete)

### 3.5 TODAY — the 60-second checklist (screen D2)
Daily items: morning weigh-in (manual number entry), meals logged count, protein progress bar, training done y/n, drinks count, bedtime target. Streak counter (7-day squares). Whole Foods Score meter (user self-scores each meal 0–100 in MVP; Plate Vision is Phase 2).
All state server-side; streak survives logout.

### 3.6 PATH — Phase 1 screen (screen N2)
"Phase 1: Foundation (wks 1–4)" — only 4 things matter: protein daily (190g), whole foods only, train 3×/week, bed by 10:45. Phase progress meter. Phases 2–4 shown LOCKED. Phase advancement is server-decided (completion criteria: 80%+ checklist adherence for the phase weeks), never client.

### 3.7 Weekly Report Card (screen L3)
Grade A–F computed server-side from: tracking honesty days, whole foods %, protein hit rate, training completion, avg battery, drinks. The climb progress bar (start BF → current → 12%). ONE focus for next week (rules engine: the single worst-performing lever). **Never ten.**

### 3.8 Locked teasers
BODY tab: "Your Body's Rules unlock after 90 days of honest data" + blurred sample curve. SCORE tab: "Capacity unlocks after your first month" + blurred ring. These sell Phase 2 inside the product.

## 4. The Battery algorithm (v1 — server-side `scoring/battery.py`)

v1 inputs (MVP data sources: manual weigh-in, checklist, survey baseline; Oura/Apple Health stubbed to manual "how did you sleep" + "energy 1–10" until Phase 2 ingestion):
```
Battery = 50 (base)
+ sleep quality (self-report 1–10 × 3, max +30)   # Phase 2: deep sleep vs baseline
+ energy (1–10 × 2, max +20)                      # Phase 2: HRV vs baseline
− drinks (count × 5, max −20)
− late dinner flag (−6)
− training strain yesterday (0/3/6 by RPE, max −12)
− missed protein yesterday (−5)
+ protein hit yesterday (+5)
+ whole foods score ≥85% yesterday (+5)
clamp 0–100. Level: <40 LOW, 40–69 GOOD, 70+ CHARGED.
```
Every component is stored with its signed contribution → the waterfall is a DB read, not a reconstruction. Store absolute values; never let display rounding corrupt stored truth (the Fade two-grades-of-truth rule).

## 5. The One Action (rules engine, `ai/coach.py` — NOT an LLM in MVP)

Priority-ordered if-chain, returns ONE action + projected battery delta:
1. drinks yesterday ≥2 → "Zero drinks today. Last night cost you ~{X} points of deep charge."
2. protein missed yesterday → "Hit {protein_target}g protein today. You're {gap}g short most days this week."
3. late dinner flag → "Dinner done by 7:30pm tonight. Late dinners are costing you ~8 battery points."
4. training due + battery ≥60 → "Train today — Push day. Your battery can carry it."
5. battery <40 → "Recovery day. Walk 20 min, bed by 10:30. Protect the streak."
6. default → "Stay the course. Protein, whole foods, bed by {bedtime}."
Tone: direct, second person, no fluff, no emoji. The coach talks users OUT of bad actions (the edge is the no).

## 6. The Doctrine (hard rules — bake into every decision)

1. **Protein never drops in a deficit.** 2. Whole foods 85%+ is the floor. 3. **Slight deficits only** — never prescribe aggressive restriction; flag crash patterns as warnings, not wins. 4. Train 3–4×/wk. 5. Sleep is the force multiplier. 6. **Trends only for body comp** — never present a single-day weight/BF reading as fact (BIA noise). 7. Bloodwork every 6 months (Phase 2). 8. **One focus per week. Never ten.**
Honesty guardrails: never the flattering number, never fake precision (all estimates labeled), never medical claims or medication content of any kind, mock data ALWAYS labeled.
Full doctrine: Obsidian vault `Claude/Projects/VOLTA/VOLTA — The Doctrine.md` — request it if anything here is ambiguous. The doctrine wins over this brief.

## 7. Data model (SQLAlchemy Core)

- `users` (id, email, pw_hash, created_at, tz)
- `survey` (user_id, outcome, age, height_in, weight_lb, bf_estimate, doctor_plan_bool, training_days, drinks_wk, diet_honesty, sleep_hours, committed_bool)
- `targets` (user_id, phase, calorie_target, protein_target_g, north_star_bf, start_bf, current_bf, bedtime, updated_at)
- `daily_logs` (user_id, date, weight_lb, sleep_quality, energy, drinks, late_dinner_bool, trained_bool, training_rpe, meals_logged, protein_g, whole_foods_score, bedtime_hit_bool)
- `battery_scores` (user_id, date, score, level, components_json) — components_json stores the waterfall rows immutably
- `weekly_reports` (user_id, week_start, grade, metrics_json, focus_text)
- Indexes on (user_id, date). All dates stored UTC, displayed in user tz.

## 8. Engineering standards (non-negotiable)

- Smallest change that solves it; match surrounding style.
- Build loop: edit source → `python3 preview/app_build.py` → extract `<script>` + `node --check` → `py_compile` backend → **serve locally + verify in a REAL browser, dark AND light, mobile viewport** → then report.
- `SECRET_KEY` and any env vars read from environment — app must fail with a clear error if unset, never silently use a dev default in production.
- Never log or expose secrets. No `.env` in repo.
- Every list/number on screen comes from the server, never fabricated client-side. Empty states say "No data yet — log today" honestly.
- Mobile hit-targets ≥44px. Test taps with `document.elementFromPoint` if anything feels dead.

## 9. Acceptance criteria (MVP done = all true)

1. New user can sign up, complete the 4-step survey, see their North Star reveal with their real numbers.
2. Battery home renders with today's score + full waterfall from stored components.
3. Checklist completes, streak increments, tomorrow's projection updates without refresh.
4. Phase 1 screen shows real progress from real logs; phases 2–4 locked.
5. Sunday: weekly report generates with a real grade + ONE focus.
6. BODY/SCORE tabs show locked teasers.
7. Dark + light themes both verified in a real mobile viewport. No console errors.
8. All scoring happens server-side; viewing page source reveals zero weights.

## 10. Explicitly OUT of scope (park for Phase 2 — do not build)

Oura/Apple Health live ingestion, Plate Vision, the Ledger curves, Capacity score, bloodwork, the Twin, course video player, womens' track, social. Stub screens only where specified.
