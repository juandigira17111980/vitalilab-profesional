from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db, limiter
from app.forms import HabitCompletionForm
from app.models import Habit, HabitEntry
from app.services.clock import local_day
from app.services.progress import complete_habit, progress_for

bp = Blueprint("habits", __name__, url_prefix="/habitos")


@bp.get("/")
@login_required
def index():
    habits = list(
        db.session.scalars(
            db.select(Habit).where(Habit.active.is_(True)).order_by(Habit.sort_order)
        )
    )
    completed_ids = set(
        db.session.scalars(
            db.select(HabitEntry.habit_id).where(
                HabitEntry.user_id == current_user.id,
                HabitEntry.completed_on == local_day(current_user),
            )
        )
    )
    return render_template(
        "habits/index.html",
        habits=habits,
        completed_ids=completed_ids,
        summary=progress_for(current_user),
        form=HabitCompletionForm(),
    )


@bp.post("/<int:habit_id>/completar")
@login_required
@limiter.limit("30 per minute")
def complete(habit_id: int):
    form = HabitCompletionForm()
    if not form.validate_on_submit():
        abort(400)
    habit = db.session.get(Habit, habit_id)
    if habit is None or not habit.active:
        abort(404)
    if complete_habit(current_user, habit):
        flash(f"¡Bien! Sumaste {habit.points} puntos con {habit.name}.", "success")
    else:
        flash("Este hábito ya estaba registrado hoy. Tus puntos no se duplicaron.", "info")
    return redirect(
        url_for("main.dashboard" if request.form.get("return_to") == "panel" else "habits.index")
    )
