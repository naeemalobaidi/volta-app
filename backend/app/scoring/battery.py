"""The Battery v1 — server-authoritative. Weights NEVER ship to the client.
Doctrine §5.1: every point explainable; components stored immutably so the
waterfall is a DB read, not a reconstruction. Absolute values only."""

BASE = 50

def level_for(score: int) -> str:
    if score < 40:
        return "LOW"
    if score < 70:
        return "GOOD"
    return "CHARGED"

def recommendation_for(level: str) -> str:
    return {
        "LOW": "Recovery day — walk, early night, protect the streak.",
        "GOOD": "Train moderate today.",
        "CHARGED": "You can push today. Make it count.",
    }[level]

def compute_battery(log: dict) -> dict:
    """log keys match daily_logs columns. Returns score + waterfall components."""
    c = []  # (label, signed_points)

    sq = log.get("sleep_quality") or 0
    pts = min(sq * 3, 30)
    c.append((f"Sleep quality {sq}/10", pts))

    en = log.get("energy") or 0
    pts = min(en * 2, 20)
    c.append((f"Energy {en}/10", pts))

    drinks = log.get("drinks") or 0
    if drinks:
        c.append((f"{drinks} drink{'s' if drinks > 1 else ''} last night", -min(drinks * 5, 20)))

    if log.get("late_dinner"):
        c.append(("Dinner after 9pm", -6))

    rpe = log.get("training_rpe") or 0
    if rpe:
        strain = -min(round(rpe * 1.2), 12)
        c.append(("Yesterday's training strain", strain))

    protein = log.get("protein_g") or 0
    target = log.get("protein_target_g") or 0
    if target:
        if protein >= target:
            c.append(("Protein target hit", 5))
        else:
            c.append((f"Protein short ({int(protein)}/{target}g)", -5))

    wfs = log.get("whole_foods_score") or 0
    if wfs >= 85:
        c.append((f"Whole foods {wfs}%", 5))

    score = BASE + sum(p for _, p in c)
    score = max(0, min(100, score))
    level = level_for(score)
    return {
        "score": score,
        "level": level,
        "recommendation": recommendation_for(level),
        "components": [{"label": l, "points": p} for l, p in c],
    }
