from __future__ import annotations

import hashlib
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from typing import Any

from flask import current_app
from flask_login import UserMixin
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy import JSON, CheckConstraint, Date, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


def utcnow() -> datetime:
    # PostgreSQL columns are deliberately timezone-naive; the stored convention is UTC.
    return datetime.now(UTC).replace(tzinfo=None)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utcnow, onupdate=utcnow, nullable=False
    )


class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('user', 'admin')", name="valid_role"),
        CheckConstraint("status IN ('active', 'inactive')", name="valid_status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="user", nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime)
    failed_login_count: Mapped[int] = mapped_column(default=0, nullable=False)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime)

    profile: Mapped[UserProfile] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    measurements: Mapped[list[HealthMeasurement]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    habit_entries: Mapped[list[HabitEntry]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def is_active(self) -> bool:
        return self.status == "active"

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    @property
    def is_locked(self) -> bool:
        return bool(self.locked_until and self.locked_until > utcnow())

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password, method="scrypt")

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def register_failed_login(self) -> None:
        self.failed_login_count += 1
        if self.failed_login_count >= 5:
            self.locked_until = utcnow() + timedelta(minutes=15)

    def register_successful_login(self) -> None:
        self.failed_login_count = 0
        self.locked_until = None
        self.last_login_at = utcnow()

    def generate_reset_token(self) -> str:
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        password_signature = hashlib.sha256(self.password_hash.encode()).hexdigest()[:16]
        return serializer.dumps(
            {"user_id": self.id, "password_signature": password_signature},
            salt="password-reset",
        )

    @classmethod
    def verify_reset_token(cls, token: str) -> User | None:
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            data = serializer.loads(
                token,
                salt="password-reset",
                max_age=current_app.config["PASSWORD_RESET_MAX_AGE"],
            )
        except (BadSignature, SignatureExpired):
            return None
        user = db.session.get(cls, data.get("user_id"))
        if user is None:
            return None
        expected = hashlib.sha256(user.password_hash.encode()).hexdigest()[:16]
        return user if data.get("password_signature") == expected else None


class UserProfile(TimestampMixin, db.Model):
    __tablename__ = "user_profiles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    display_name: Mapped[str] = mapped_column(String(80), nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date)
    grade: Mapped[str | None] = mapped_column(String(80))
    timezone: Mapped[str] = mapped_column(String(50), default="America/Bogota", nullable=False)
    privacy_version: Mapped[str] = mapped_column(String(20), default="2026-09", nullable=False)
    privacy_accepted_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="profile")


class HealthMeasurement(db.Model):
    __tablename__ = "health_measurements"
    __table_args__ = (
        CheckConstraint("weight_kg BETWEEN 20 AND 500", name="valid_weight"),
        CheckConstraint("height_cm BETWEEN 80 AND 250", name="valid_height"),
        CheckConstraint("bmi_snapshot BETWEEN 5 AND 100", name="valid_bmi"),
        db.Index("ix_health_measurements_user_measured_on", "user_id", "measured_on"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    weight_kg: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    height_cm: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    bmi_snapshot: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    measured_on: Mapped[date] = mapped_column(Date, default=date.today, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="measurements")


class Habit(TimestampMixin, db.Model):
    __tablename__ = "habits"
    __table_args__ = (CheckConstraint("points BETWEEN 1 AND 100", name="valid_points"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(280), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    icon: Mapped[str] = mapped_column(String(20), nullable=False)
    points: Mapped[int] = mapped_column(default=15, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
    sort_order: Mapped[int] = mapped_column(default=0, nullable=False)

    entries: Mapped[list[HabitEntry]] = relationship(back_populates="habit")


class HabitEntry(db.Model):
    __tablename__ = "habit_entries"
    __table_args__ = (
        db.UniqueConstraint("user_id", "habit_id", "completed_on", name="uq_habit_daily"),
        db.Index("ix_habit_entries_user_completed_on", "user_id", "completed_on"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    habit_id: Mapped[int] = mapped_column(
        ForeignKey("habits.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    completed_on: Mapped[date] = mapped_column(Date, default=date.today, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="habit_entries")
    habit: Mapped[Habit] = relationship(back_populates="entries")


class Announcement(TimestampMixin, db.Model):
    __tablename__ = "announcements"
    __table_args__ = (
        CheckConstraint("status IN ('draft', 'published', 'archived')", name="valid_status"),
        db.Index("ix_announcements_status_published_at", "status", "published_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    author_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="draft", index=True, nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime, index=True)

    author: Mapped[User] = relationship()


class AuditEvent(db.Model):
    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    actor_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    action: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str | None] = mapped_column(String(80))
    metadata_redacted: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utcnow, index=True, nullable=False
    )

    actor: Mapped[User | None] = relationship()


class UserGoal(TimestampMixin, db.Model):
    __tablename__ = "user_goals"
    __table_args__ = (
        db.UniqueConstraint("user_id", "habit_id", name="uq_user_goal_habit"),
        CheckConstraint("target_days BETWEEN 1 AND 7", name="valid_target_days"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    habit_id: Mapped[int] = mapped_column(
        ForeignKey("habits.id", ondelete="RESTRICT"), nullable=False
    )
    target_days: Mapped[int] = mapped_column(nullable=False)
    habit: Mapped[Habit] = relationship()


class DailyCheckIn(TimestampMixin, db.Model):
    __tablename__ = "daily_checkins"
    __table_args__ = (
        db.UniqueConstraint("user_id", "checked_on", name="uq_user_daily_checkin"),
        CheckConstraint("energy BETWEEN 1 AND 5", name="valid_energy"),
        CheckConstraint("focus BETWEEN 1 AND 5", name="valid_focus"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    checked_on: Mapped[date] = mapped_column(Date, nullable=False)
    energy: Mapped[int] = mapped_column(nullable=False)
    focus: Mapped[int] = mapped_column(nullable=False)


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return db.session.get(User, int(user_id)) if user_id.isdigit() else None
