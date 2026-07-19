"""Weekly report card — ONE grade, ONE focus. Never ten."""
from datetime import date, timedelta

def grade_from(pct: float) -> str:
    if pct >= 90: return "A"
    if pct >= 80: return "A−"
    if pct >= 70: return "B"
    if pct >= 55: return "C"
    if pct >= 40: return "D"
    return "F"

def build_weekly_report(logs: list, targets: dict) -> dict:
    """logs: up to 7 daily_log dicts for the week."""
    days = len(logs) or 1
    protein_target = targets.get("protein_target_g") or 1

    tracking = sum(1 for l in logs if l.get("weight_lb") or l.get("meals_logged"))
    protein_hits = sum(1 for l in logs if (l.get("protein_g") or 0) >= protein_target)
    trained = sum(1 for l in logs if l.get("trained"))
    wf_scores = [l.get("whole_foods_score") or 0 for l in logs]
    avg_wf = sum(wf_scores) / days
    drinks = sum(l.get("drinks") or 0 for l in logs)
    avg_battery = sum(l.get("battery_score") or 0 for l in logs) / days

    metrics = {
        "tracking_days": f"{tracking}/7",
        "whole_foods_avg": round(avg_wf),
        "protein_hit_rate": f"{protein_hits}/7",
        "training_sessions": trained,
        "avg_battery": round(avg_battery),
        "drinks": drinks,
    }

    # Weighted adherence → grade
    pct = (tracking / 7 * 30 + protein_hits / 7 * 30 + min(trained, 3) / 3 * 20
           + min(avg_wf, 100) / 100 * 20)
    grade = grade_from(pct * 100 / 100)

    # ONE focus: the single worst lever
    levers = sorted([
        (tracking / 7, "Log honestly, every day. 60 seconds. That's the deal."),
        (protein_hits / 7, f"Hit {protein_target}g protein daily. Nothing else matters more this week."),
        (min(trained, 3) / 3, "Get your 3 training sessions in. Muscle is the metabolism."),
        (avg_wf / 100, "Whole foods only this week. Nothing in a wrapper."),
    ], key=lambda x: x[0])
    focus = levers[0][1]

    return {"grade": grade, "metrics": metrics, "focus_text": focus,
            "week_start": str(date.today() - timedelta(days=date.today().weekday()))}
