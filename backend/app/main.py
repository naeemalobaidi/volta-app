"""VOLTA API — server is the source of truth. Client displays; server decides."""
import json
from datetime import date, datetime, timedelta

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from sqlalchemy import select, insert, update

from .db import engine, init_db
from .db.models import users, survey, targets, daily_logs, battery_scores, weekly_reports
from .auth import hash_password, verify_password, make_token, read_token
from .scoring.battery import compute_battery
from .scoring.targets import derive_targets
from .scoring.weekly import build_weekly_report
from .ai.coach import one_action

app = FastAPI(title="VOLTA", docs_url=None, redoc_url=None)
init_db()


# ---------- helpers ----------

def current_user_id(req: Request) -> int:
    auth = req.headers.get("authorization", "")
    token = auth.removeprefix("Bearer ").strip()
    uid = read_token(token) if token else None
    if not uid:
        raise HTTPException(401, "Not authenticated")
    return uid

def row_to_dict(r) -> dict | None:
    return dict(r._mapping) if r is not None else None

def get_targets(conn, uid: int) -> dict:
    return row_to_dict(conn.execute(select(targets).where(targets.c.user_id == uid)).first()) or {}

def get_log(conn, uid: int, d: date) -> dict:
    r = conn.execute(select(daily_logs).where(
        daily_logs.c.user_id == uid, daily_logs.c.date == d)).first()
    return row_to_dict(r) or {}

def battery_for_date(conn, uid: int, d: date) -> dict:
    r = conn.execute(select(battery_scores).where(
        battery_scores.c.user_id == uid, battery_scores.c.date == d)).first()
    if r:
        row = row_to_dict(r)
        row["components"] = json.loads(row.pop("components_json"))
        return row
    return {}


# ---------- auth ----------

class Cred(BaseModel):
    email: EmailStr
    password: str

@app.post("/api/signup")
def signup(c: Cred):
    with engine.begin() as conn:
        if conn.execute(select(users).where(users.c.email == c.email)).first():
            raise HTTPException(409, "Account exists — log in instead")
        cur = conn.execute(insert(users).values(email=c.email, pw_hash=hash_password(c.password)))
        uid = cur.inserted_primary_key[0]
    return {"token": make_token(uid)}

@app.post("/api/login")
def login(c: Cred):
    with engine.connect() as conn:
        r = conn.execute(select(users).where(users.c.email == c.email)).first()
        if not r or not verify_password(c.password, r.pw_hash):
            raise HTTPException(401, "Wrong email or password")
        return {"token": make_token(r.id)}


# ---------- survey → targets ----------

class SurveyIn(BaseModel):
    outcome: str
    age: int
    height_in: float
    weight_lb: float
    bf_estimate: float | None = None
    doctor_plan: bool = False
    training_days: int
    drinks_wk: int
    diet_honesty: str
    sleep_hours: str
    committed: bool

@app.post("/api/survey")
def save_survey(s: SurveyIn, req: Request):
    uid = current_user_id(req)
    data = s.model_dump()
    t = derive_targets(data)
    with engine.begin() as conn:
        conn.execute(insert(survey).values(user_id=uid, **data)
                     .prefix_with("OR REPLACE") if engine.dialect.name == "sqlite"
                     else insert(survey).values(user_id=uid, **data))
        existing = get_targets(conn, uid)
        if existing:
            conn.execute(update(targets).where(targets.c.user_id == uid).values(**t))
        else:
            conn.execute(insert(targets).values(user_id=uid, **t))
    return {"ok": True, "targets": t}


# ---------- today ----------

class LogIn(BaseModel):
    date: str | None = None
    weight_lb: float | None = None
    sleep_quality: int | None = None
    energy: int | None = None
    drinks: int | None = None
    late_dinner: bool | None = None
    trained: bool | None = None
    training_rpe: int | None = None
    meals_logged: int | None = None
    protein_g: float | None = None
    whole_foods_score: int | None = None
    bedtime_hit: bool | None = None

@app.post("/api/log")
def upsert_log(body: LogIn, req: Request):
    uid = current_user_id(req)
    d = date.fromisoformat(body.date) if body.date else date.today()
    data = {k: v for k, v in body.model_dump().items() if v is not None and k != "date"}
    with engine.begin() as conn:
        existing = get_log(conn, uid, d)
        if existing:
            conn.execute(update(daily_logs).where(
                daily_logs.c.user_id == uid, daily_logs.c.date == d).values(**data))
        else:
            conn.execute(insert(daily_logs).values(user_id=uid, date=d, **data))
        # recompute battery for the day from merged state
        merged = {**existing, **data}
        merged["protein_target_g"] = get_targets(conn, uid).get("protein_target_g")
        b = compute_battery(merged)
        stored = {"user_id": uid, "date": d, "score": b["score"], "level": b["level"],
                  "components_json": json.dumps(b["components"])}
        if battery_for_date(conn, uid, d):
            conn.execute(update(battery_scores).where(
                battery_scores.c.user_id == uid, battery_scores.c.date == d).values(**stored))
        else:
            conn.execute(insert(battery_scores).values(**stored))
    return {"ok": True, "battery": b}

@app.get("/api/today")
def today(req: Request):
    uid = current_user_id(req)
    d = date.today()
    with engine.connect() as conn:
        t = get_targets(conn, uid)
        log = get_log(conn, uid, d)
        batt = battery_for_date(conn, uid, d)
        y_log = get_log(conn, uid, d - timedelta(days=1))
        y_batt = battery_for_date(conn, uid, d - timedelta(days=1))

        # streak: consecutive days with any log, ending today/yesterday
        streak, cur = 0, d
        while get_log(conn, uid, cur):
            streak += 1
            cur -= timedelta(days=1)

        projection = None
        if batt:
            ctx = {"yesterday": y_log or log, "targets": t, "battery": batt}
            act = one_action(ctx)
            projection = min(100, batt["score"] + act["projected_delta"])
        else:
            act = one_action({"yesterday": y_log, "targets": t, "battery": y_batt or {"score": 50}})

        return {
            "date": str(d),
            "targets": t,
            "log": log,
            "battery": batt or None,
            "streak": streak,
            "one_action": act,
            "tomorrow_projection": projection,
            "phase": {"number": t.get("phase", 1), "week": t.get("phase_week", 1),
                      "name": {1: "Foundation", 2: "The Deficit", 3: "The Refinement", 4: "Maintenance"}.get(t.get("phase", 1), "Foundation")},
        }


# ---------- weekly report ----------

@app.get("/api/weekly")
def weekly(req: Request):
    uid = current_user_id(req)
    week_start = date.today() - timedelta(days=date.today().weekday())
    with engine.begin() as conn:
        r = conn.execute(select(weekly_reports).where(
            weekly_reports.c.user_id == uid, weekly_reports.c.week_start == week_start)).first()
        if r:
            row = row_to_dict(r)
            row["metrics"] = json.loads(row.pop("metrics_json"))
            return row
        logs = []
        for i in range(7):
            l = get_log(conn, uid, week_start + timedelta(days=i))
            if l:
                b = battery_for_date(conn, uid, week_start + timedelta(days=i))
                l["battery_score"] = b.get("score", 0)
                logs.append(l)
        report = build_weekly_report(logs, get_targets(conn, uid))
        conn.execute(insert(weekly_reports).values(
            user_id=uid, week_start=week_start, grade=report["grade"],
            metrics_json=json.dumps(report["metrics"]), focus_text=report["focus_text"]))
        report["metrics"] = report["metrics"]
        return report


# ---------- static ----------

import pathlib
preview_dir = pathlib.Path(__file__).resolve().parents[2] / "preview"

@app.get("/")
def index():
    html = preview_dir / "app.html"
    if html.exists():
        return FileResponse(html)
    return JSONResponse({"status": "VOLTA API running — frontend not built yet"})
