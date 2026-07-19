"""The One Action — rules engine, NOT an LLM. Doctrine §8: the coach talks
users OUT of bad actions. One action, never ten. Direct second-person tone."""

def one_action(ctx: dict) -> dict:
    """ctx: yesterday_log, streak, targets, battery. Returns action + projected delta."""
    y = ctx.get("yesterday") or {}
    t = ctx.get("targets") or {}
    b = ctx.get("battery") or {}
    protein_target = t.get("protein_target_g", 0)
    bedtime = t.get("bedtime", "22:45")

    if (y.get("drinks") or 0) >= 2:
        return {"action": f"Zero drinks today. Last night cost you ~{min(y['drinks']*5,20)} points of deep charge.",
                "projected_delta": 9}
    if protein_target and (y.get("protein_g") or 0) < protein_target:
        gap = protein_target - (y.get("protein_g") or 0)
        return {"action": f"Hit {protein_target}g protein today. You were {int(gap)}g short yesterday.",
                "projected_delta": 5}
    if y.get("late_dinner"):
        return {"action": "Dinner done by 7:30pm tonight. Late dinners cost you ~8 battery points.",
                "projected_delta": 6}
    if b.get("score", 0) < 40:
        return {"action": f"Recovery day. Walk 20 minutes, bed by {bedtime}. Protect the streak.",
                "projected_delta": 12}
    if b.get("score", 0) >= 60 and not y.get("trained"):
        return {"action": "Train today. Your battery can carry it — make it count.",
                "projected_delta": 4}
    return {"action": f"Stay the course. Protein, whole foods, bed by {bedtime}.",
            "projected_delta": 2}
