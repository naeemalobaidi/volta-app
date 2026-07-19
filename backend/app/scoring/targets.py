"""Targets — derived from survey. Server-side only.
Doctrine: slight deficits only (Phase 2+), protein ≈ 1g/lb goal BW, never crash."""

ACTIVITY_FACTOR = 1.35

def mifflin_st_jeor(weight_lb: float, height_in: float, age: int, sex: str = "male") -> float:
    kg = weight_lb * 0.453592
    cm = height_in * 2.54
    base = 10 * kg + 6.25 * cm - 5 * age
    return base + 5 if sex == "male" else base - 161

def derive_targets(survey: dict) -> dict:
    weight = survey["weight_lb"]
    height = survey["height_in"]
    age = survey["age"]
    bf = survey.get("bf_estimate") or estimate_bf(weight, height, age)

    tdee = mifflin_st_jeor(weight, height, age) * ACTIVITY_FACTOR

    # Phase 1 = Foundation: eat at maintenance, install habits. NO deficit yet.
    calorie_target = round(tdee / 50) * 50

    # Goal weight = lean mass carried at 12% BF (the North Star)
    lean_mass = weight * (1 - bf / 100)
    goal_weight = round(lean_mass / (1 - 0.12), 1)
    protein_target = round(goal_weight)  # ~1g per lb of GOAL body weight

    return {
        "phase": 1,
        "phase_week": 1,
        "calorie_target": calorie_target,
        "protein_target_g": protein_target,
        "north_star_bf": 12.0,
        "start_bf": bf,
        "current_bf": bf,
        "goal_weight_lb": goal_weight,
        "bedtime": "22:45",
    }

def estimate_bf(weight_lb: float, height_in: float, age: int) -> float:
    """Rough navy-style placeholder until scale data flows. Labeled estimate."""
    bmi = weight_lb / (height_in ** 2) * 703
    return round(max(10.0, min(45.0, 1.20 * bmi + 0.23 * age - 16.2)), 1)
