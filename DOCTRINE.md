---
categories:
  - "[[Projects]]"
  - "[[Health]]"
created: 2026-07-18
up: "[[VOLTA — Project Overview]]"
related: "[[VOLTA — Product Concept]]"
---

# VOLTA — The Doctrine (framework-lens)

> **Name locked: VOLTA.** Four meanings, one product: (1) the volt / Alessandro Volta, inventor of the battery — the core product is a battery for your body; (2) volta = "the turn" (Italian) — the turn your body needed, the turning point in the user's story; (3) voltage vs capacity — the two scores map onto the physics (Battery = today's charge, Capacity = the size of the cell); (4) brandable — four letters, global, zero health-app cliché. Tagline candidates: "Know your charge." / "The turn your body needed." / "Energy, measured honestly."
>
> The single most important artifact in the project. This document IS the product spec, the scoring algorithm's brain, the AI coach's system prompt, and the coaching rules. When a feature question arises, the answer is here. One live copy — once the repo exists, this moves there and everything points to it.

---

## 0. The product in one sentence

VOLTA turns six daily data streams into one honest number, one daily action, and long-term proof — built around a single keystone: **reaching and holding 10–12% body fat (men) / ~18–22% (women), the highest-leverage longevity variable a person controls.**

The product is not a tracker. It is a **faithful, executable expression of one method**: whole-foods nutrition, protein guarded, honest training, sleep as force multiplier, bloodwork as audit — with the truth shown even when it's unflattering.

---

## 1. The core edge (why this wins)

Every health app owns ONE loop (sleep, food, training, blood, weight). Nobody owns the causal chain between them. Our edge:

1. **Cross-domain causation.** Six streams in one brain → personal dose-response curves ("2 drinks = −19% deep sleep, +6 bpm sleeping HR — for YOU"). Nobody else can say this sentence to their user.
2. **Explainable scoring.** Every number shows its work (the waterfall). Black-box scores (Oura, Whoop) train distrust; ours trains belief.
3. **Fat-vs-muscle truth.** The scale lies; we decompose it weekly (fat / muscle / water). In the GLP-1 era this is THE unanswered question of the largest weight-loss cohort in history.
4. **Blood-validated predictions.** Forecast the panel months out; the draw grades the system. Trust compounds every 6 months.
5. **Honesty as retention.** The app talks users OUT of bad decisions (training through illness, crash deficits, "wine helps me sleep"). The edge is the *no*.

---

## 2. The North Star

**10–12% body fat.** Not aesthetics — the zone where visceral fat clears, insulin sensitivity resets, inflammation and hormones normalize, and every longevity marker moves at once.

- Every screen, phase, and coach note ultimately points at the climb to the North Star.
- Pace doctrine: **slight deficit** (~300–500 kcal), never crash. Crash deficits burn muscle — the cardinal sin.
- Arrival is not the end: **maintenance is the product.** The "after" is pre-built before the user needs it.

---

## 3. The hard rules (non-negotiable — the app enforces these, always)

1. **Protein never drops in a deficit.** Target ≈ 1g per lb of goal body weight. In a deficit protein protects muscle; in a surplus it builds it.
2. **Whole foods are the floor, not the ceiling.** 85%+ Whole Foods Score daily. If it grew/walked/swam/flew it's food; if it has a marketing department it's suspect.
3. **Slight deficits only.** ~300–500 kcal. Aggressive deficits are treated by the app as a *bug to correct*, not willpower to praise.
4. **Train 3–4×/week, log everything.** Muscle is the metabolism; the app weighs stimulus vs recovery before recommending intensity.
5. **Sleep is the force multiplier.** Short sleep → +appetite, −training quality, fat-vs-muscle loss ratio worsens. The app quantifies this with the user's own data.
6. **Same-time daily weigh-in; the trend is the truth.** BIA scales are noisy point-to-point — the app NEVER shows a single-day body-fat reading as fact. Trends only.
7. **Bloodwork every 6 months.** The audit. The app predicts it, explains it, and is graded by it.
8. **One focus per week. Never ten.** The coach corrects like a great coach — one thing at a time.

---

## 4. The honesty guardrails (what the app must refuse to do)

- **Never recommend, name, or hint at medication.** Doctor's lane is doctor's lane. If the user is on a doctor-supervised plan, we track the body's response — nothing more. (See [[VOLTA — GLP-1 Positioning]].)
- **Never show the flattering number.** BIA single-day readings, pre-trend weight spikes, "you lost 8 lbs!" without the fat/muscle decomposition — all banned.
- **Never fake precision.** Forecasts carry confidence ranges; dose-response curves state sample size and pattern confidence.
- **Never medical-claim.** Wellness positioning throughout; "your data, finally explained" — not diagnosis, not treatment.
- **Never celebrate a crash.** Scale dropping fast with lean-mass decline triggers a warning, not a confetti animation.
- **Never let a streak override biology.** If The Guard detects illness signals, the streak is protected while training is swapped. Discipline ≠ self-harm.

---

## 5. The scoring brain (how the numbers are built)

### 5.1 The Battery (daily, 0–100) — *how much you have today*
Charged by: deep sleep duration vs baseline, HRV vs personal baseline, sleep timing/regularity, micronutrient sufficiency (rolling 7-day).
Drained by: training strain (volume × intensity vs recovery capacity), daytime stress load, alcohol (dose-scaled), late meals, illness signals.
- **Every point is explainable.** The waterfall IS the product: "+14 deep sleep, −9 alcohol, −6 late dinner = 71."
- Output = number + ONE action. Never a dashboard.
- Tomorrow's projected battery updates live as the day is logged (the habit loop).

### 5.2 Capacity (monthly re-baseline, 0–100) — *is your biology improving*
Inputs (slow signals only): trend HRV (90d), resting HR trend, strength progression (e1RM), lean-mass trend, visceral fat trend, body-fat % vs North Star, latest blood panel vs optimal.
- Cannot be gamed by one good week. Moves only when the user truly moves it.
- Validated against Quest panels every 6 months → the "proven score."
- Derived display: **estimated body age** (calendar vs biological). Trending younger = the bragging right.

### 5.3 The Ledger (personal dose-response)
- Computed per-user after ~90 days of honest data: alcohol→deep sleep, caffeine cutoff→sleep, sleep debt→next-day intake, protein×training→lean mass, meal timing→battery.
- Every curve carries: sample size, confidence, and the date it was last re-computed.
- New rules unlock as data matures — the retention weapon.

### 5.4 The Twin (simulation engine)
- "What if I cut alcohol 30 days?" → projected BF, battery, sleep, North Star arrival — computed from the user's own Ledger curves, never population averages.

### 5.5 Fat-Purity Verdict (weekly)
- Weight change decomposed into fat / muscle / water (scale trend + training performance + protein adherence + sodium/water context).
- The verdict line speaks plainly: "94% pure fat loss — keep going" or "muscle loss detected — correction inside."
- **This screen is the GLP-1 cohort's reason to exist in the app.**

### 5.6 The Guard (anomaly detection)
- Temp + resting HR + respiratory rate + HRV divergence vs baseline, 48–72h pre-symptom.
- Doesn't just warn — **rewrites the plan** (swaps lift → walk), protects the streak, and references the last ignored warning.

### 5.7 Bloodwork forecast
- Six months of behavior → per-marker directional forecast with confidence. Post-draw: predicted vs actual, accuracy shown publicly (trust builder).

---

## 6. The course (the doctrine taught)

Six 9-minute modules, drip-released with the phases (full text in [[VOLTA — The Course]]):
1. Why 12% — the target explained
2. Deficit & surplus — the only dial (slight deficit to lose, slight surplus of whole foods to build)
3. Protein — the non-negotiable
4. Read any label in 5 seconds (protein high? added sugar ~0? ingredients you'd buy separately?)
5. Whole foods vs the wrapper
6. Sleep, training & the long game

Teaching principles: one idea per module, teach the skill not the restriction, every lesson enforced by the app the same day.

---

## 7. The phases (the climb)

- **Phase 1 — Foundation (wks 1–4):** protein daily, whole foods, 3× training, bedtime. NO restriction. Install the floor first.
- **Phase 2 — The Deficit:** slight deficit engages; protein guarded; fat-purity verdict weekly.
- **Phase 3 — The Refinement:** Ledger curves mature; meal timing, alcohol, caffeine tuned to the user's own data.
- **Phase 4 — 12% & Maintenance for life:** the dial flips to maintenance; the app's job becomes keeping the truth visible forever.
- Phases unlock by completion, not time. The plan adapts weekly from data.

---

## 8. The GLP-1 rider (hard positioning rules)

The largest weight-loss cohort in history is arriving. We serve them without naming anything:
- Hook: "Everyone's losing weight. Most are losing the wrong thing." / "Lose weight. Just make sure it's fat."
- The survey asks neutrally: "working with a doctor on a weight-management plan?" → routes to the muscle-guard track.
- Their hero screen = the Fat-Purity Verdict. Their hard rules = protein + training, enforced harder.
- The Exit Ramp: when the doctor's plan winds down, maintenance numbers, food skills, and body rules are already in place. Regain-proofed before they need it.

---

## 9. What we refuse to build (the parked list)

- Social feeds, likes, comments (leaderboards maybe Phase 2 — gamification is not the product).
- Our own hardware (Oura/Apple Health already shipped the sensors; zero COGS is the moat).
- Meal plans/recipes content farm (the label rule replaces recipes).
- Any medical/advisory feature (stays wellness-side of the line).
- Calorie math exposed to the user (the app turns the dial; the user never does math).

---

## 10. Collaboration contract for all agents on this project

- This doctrine is the source of truth. Feature question → answer is here first.
- Smallest change that solves it. Match surrounding style.
- Server is the source of truth: scores, body decomposition, and AI context are computed server-side; the client displays. Proprietary logic NEVER ships to the client.
- Every external data source: cache + last-good + fallback from day one.
- Verify in a real browser (dark AND light, mobile viewport) before "done."
- Mock data is ALWAYS labeled as mock.
- Honesty beats flattery — in the product and in the build room.
