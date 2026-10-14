from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db, limiter
from app.forms import CheckInForm, EmptyForm, GoalForm
from app.models import DailyCheckIn, Habit, UserGoal
from app.services.progress import progress_for
from app.services.wellness import (
    goals_for,
    history_for,
    local_day,
    remove_goal,
    save_checkin,
    save_goal,
)
from app.wellness.catalog import ROUTINES

bp = Blueprint("wellness", __name__)


@bp.route("/metas/", methods=["GET", "POST"])
@login_required
@limiter.limit("30 per minute", methods=["POST"])
def goals():
    form = GoalForm()
    habits = list(
        db.session.scalars(
            db.select(Habit).where(Habit.active.is_(True)).order_by(Habit.sort_order)
        )
    )
    form.habit_id.choices = [(habit.id, habit.name) for habit in habits]
    if form.validate_on_submit():
        habit = next(habit for habit in habits if habit.id == form.habit_id.data)
        if save_goal(current_user, habit, form.target_days.data):
            flash("Meta guardada. Tu progreso se calcula con los últimos siete días.", "success")
            return redirect(url_for("wellness.goals"))
        flash(
            "Otra solicitud acaba de guardar esta meta. Revisa el resultado y vuelve a intentarlo.",
            "info",
        )
    elif request.method == "POST":
        flash("Revisa los campos marcados antes de guardar tu meta.", "error")
    return render_template(
        "wellness/goals.html", form=form, goals=goals_for(current_user), empty_form=EmptyForm()
    )


@bp.post("/metas/<int:goal_id>/eliminar")
@login_required
@limiter.limit("30 per minute")
def delete_goal(goal_id):
    if not EmptyForm().validate_on_submit():
        abort(400)
    goal = db.session.scalar(
        db.select(UserGoal).where(UserGoal.id == goal_id, UserGoal.user_id == current_user.id)
    )
    if goal is None:
        abort(404)
    remove_goal(goal, current_user)
    flash("Meta retirada. Tus hábitos registrados se conservan.", "success")
    return redirect(url_for("wellness.goals"))


@bp.route("/bitacora/", methods=["GET", "POST"])
@login_required
@limiter.limit("30 per minute", methods=["POST"])
def checkin():
    existing = db.session.scalar(
        db.select(DailyCheckIn).where(
            DailyCheckIn.user_id == current_user.id,
            DailyCheckIn.checked_on == local_day(current_user),
        )
    )
    form = CheckInForm(obj=existing)
    if form.validate_on_submit():
        if save_checkin(current_user, form.energy.data, form.focus.data):
            flash("Registro guardado. Puedes actualizarlo hoy sin crear duplicados.", "success")
            return redirect(url_for("wellness.checkin"))
        flash("El registro cambió en otra solicitud. Recarga y comprueba tus valores.", "info")
    elif request.method == "POST":
        flash("Selecciona un valor válido en cada campo.", "error")
    return render_template(
        "wellness/checkin.html", form=form, existing=existing, history=history_for(current_user)
    )


@bp.get("/progreso/")
@login_required
def progress():
    return render_template(
        "wellness/progress.html",
        summary=progress_for(current_user),
        history=history_for(current_user),
        goals=goals_for(current_user),
    )


@bp.get("/rutinas/")
def library():
    query = request.args.get("q", "")[:80].strip()
    category = request.args.get("categoria", "")
    routines = [
        routine
        for routine in ROUTINES
        if (not category or routine["category"] == category)
        and query.casefold() in (routine["name"] + " " + routine["description"]).casefold()
    ]
    return render_template(
        "wellness/library.html",
        routines=routines,
        query=query,
        category=category,
        categories=("Calma", "Movimiento", "Descanso", "Enfoque"),
    )


@bp.get("/rutinas/<slug>/")
def routine(slug):
    selected = next((item for item in ROUTINES if item["slug"] == slug), None)
    if selected is None:
        abort(404)
    habit = db.session.scalar(
        db.select(Habit).where(Habit.code == selected["habit_code"], Habit.active.is_(True))
    )
    return render_template("wellness/routine.html", routine=selected, habit=habit)
