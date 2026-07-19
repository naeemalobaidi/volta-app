"""Data model — SQLAlchemy Core. All dates UTC; display tz is a client concern."""
from sqlalchemy import (MetaData, Table, Column, Integer, String, Float,
                        Boolean, Date, DateTime, Text, Index, func)

metadata = MetaData()

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, nullable=False),
    Column("pw_hash", String, nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
    Column("tz", String, default="UTC"),
)

survey = Table(
    "survey", metadata,
    Column("user_id", Integer, primary_key=True),
    Column("outcome", String),            # longevity | lean | energy | bloodwork
    Column("age", Integer),
    Column("height_in", Float),
    Column("weight_lb", Float),
    Column("bf_estimate", Float),         # nullable — "measure it for me"
    Column("doctor_plan", Boolean, default=False),  # stored, never acted on medically
    Column("training_days", Integer),
    Column("drinks_wk", Integer),
    Column("diet_honesty", String),       # whole | half | packaged
    Column("sleep_hours", String),        # <6 | 6-7 | 7+
    Column("committed", Boolean, default=False),
)

targets = Table(
    "targets", metadata,
    Column("user_id", Integer, primary_key=True),
    Column("phase", Integer, default=1),  # 1 Foundation … 4 Maintenance
    Column("phase_week", Integer, default=1),
    Column("calorie_target", Integer),
    Column("protein_target_g", Integer),
    Column("north_star_bf", Float, default=12.0),
    Column("start_bf", Float),
    Column("current_bf", Float),
    Column("goal_weight_lb", Float),
    Column("bedtime", String, default="22:45"),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)

daily_logs = Table(
    "daily_logs", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("date", Date, nullable=False),
    Column("weight_lb", Float),
    Column("sleep_quality", Integer),     # 1–10 (Phase 2: Oura-derived)
    Column("energy", Integer),            # 1–10 (Phase 2: HRV-derived)
    Column("drinks", Integer, default=0),
    Column("late_dinner", Boolean, default=False),
    Column("trained", Boolean, default=False),
    Column("training_rpe", Integer, default=0),  # 0–10
    Column("meals_logged", Integer, default=0),
    Column("protein_g", Float, default=0),
    Column("whole_foods_score", Integer, default=0),  # 0–100
    Column("bedtime_hit", Boolean, default=False),
    Index("ix_daily_user_date", "user_id", "date", unique=True),
)

battery_scores = Table(
    "battery_scores", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("date", Date, nullable=False),
    Column("score", Integer, nullable=False),
    Column("level", String, nullable=False),   # LOW | GOOD | CHARGED
    Column("components_json", Text, nullable=False),  # immutable waterfall rows
    Index("ix_battery_user_date", "user_id", "date", unique=True),
)

weekly_reports = Table(
    "weekly_reports", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("week_start", Date, nullable=False),
    Column("grade", String, nullable=False),   # A … F
    Column("metrics_json", Text, nullable=False),
    Column("focus_text", Text),                # ONE focus. Never ten.
    Index("ix_weekly_user_week", "user_id", "week_start", unique=True),
)
