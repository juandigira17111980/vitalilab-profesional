from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db, limiter
from app.forms import CheckInForm, EmptyForm, GoalForm
from app.models import DailyCheckIn, Habit, UserGoal
from app.services.personal_routines import (
    archive_personal_routine,
    owned_routine,
    personal_routines_for,
    save_personal_routine,
)
from app.services.progress import progress_for
from app.services.wellness import (
    goals_for,
    history_for,
    local_day,
    remove_goal,
    save_checkin,
    save_goal,
)
from app.wellness.catalog import ROUTINES, VISUALS
from app.wellness.forms import GOAL_CHOICES, PersonalRoutineForm

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
    personal_view = request.args.get("para") == "mi"
    goal = request.args.get("objetivo", "")
    preference = "adaptable"
    if personal_view:
        category = ""
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=url_for("wellness.library", para="mi")))
        if not current_user.profile.personalization_completed_at:
            return redirect(url_for("profile.setup_measurement"))
        goal = current_user.profile.movement_goal
        preference = current_user.profile.movement_preference
    if goal not in dict(GOAL_CHOICES):
        goal = ""
    routines = [
        routine
        for routine in ROUTINES
        if (not category or routine["category"] == category)
        and (not goal or routine["goal"] == goal)
        and (preference == "adaptable" or preference in routine["preferences"])
        and query.casefold() in (routine["name"] + " " + routine["description"]).casefold()
    ]
    return render_template(
        "wellness/library.html",
        routines=routines,
        query=query,
        category=category,
        categories=("Calma", "Movimiento", "Descanso", "Enfoque"),
        personal_view=personal_view,
        goal=goal,
        goals=GOAL_CHOICES,
        visuals=VISUALS,
        own_routines=personal_routines_for(current_user) if current_user.is_authenticated else [],
    )


@bp.get("/rutinas/<slug>/")
def routine(slug):
    selected = next((item for item in ROUTINES if item["slug"] == slug), None)
    if selected is None:
        abort(404)
    habit = db.session.scalar(
        db.select(Habit).where(Habit.code == selected["habit_code"], Habit.active.is_(True))
    )
    from app.services.movement import routine_done_today

    return render_template(
        "wellness/routine.html",
        routine=selected,
        habit=habit,
        completed=current_user.is_authenticated and routine_done_today(current_user, slug),
        visuals=VISUALS,
    )


@bp.post("/rutinas/<slug>/registrar")
@login_required
@limiter.limit("30 per minute")
def complete_routine(slug):
    from app.services.movement import register_routine

    if not EmptyForm().validate_on_submit():
        abort(400)
    if not any(item["slug"] == slug for item in ROUTINES):
        abort(404)
    result = register_routine(current_user, slug)
    if result is None:
        abort(404)
    if not result["created"]:
        flash("Esta rutina ya está registrada hoy; no duplicamos puntos.", "info")
    elif result["points"]:
        flash(f"Rutina registrada. +{result['points']} XP por tu constancia.", "success")
    else:
        flash("Rutina registrada. El hábito asociado ya había sumado sus puntos hoy.", "success")
    return redirect(
        url_for("profile.edit")
        if request.form.get("origin") == "profile"
        else url_for("wellness.routine", slug=slug)
    )


@bp.route("/mis-rutinas/nueva", methods=["GET", "POST"])
@bp.route("/mis-rutinas/<int:routine_id>/editar", methods=["GET", "POST"])
@login_required
@limiter.limit("40 per hour", methods=["POST"])
def edit_personal_routine(routine_id=None):
    routine = owned_routine(current_user, routine_id) if routine_id is not None else None
    if routine_id is not None and routine is None:
        abort(404)
    form = PersonalRoutineForm(obj=routine)
    if request.method == "POST" and request.form.get("intent") == "add-exercise":
        if len(form.exercises) < 12:
            form.exercises.append_entry()
        else:
            flash("Puedes guardar hasta 12 ejercicios por rutina.", "info")
    elif form.validate_on_submit():
        try:
            saved = save_personal_routine(current_user, form.data, routine_id)
        except LookupError:
            abort(404)
        except ValueError as error:
            db.session.rollback()
            flash(str(error), "error")
            return render_template("wellness/personal_edit.html", form=form, routine=routine), 409
        flash("Tu rutina está guardada. Solo tú puedes verla y editarla.", "success")
        return redirect(url_for("wellness.personal_routine", routine_id=saved.id))
    elif form.is_submitted():
        flash("Revisa los campos marcados. No se ha guardado la rutina.", "error")
    return render_template("wellness/personal_edit.html", form=form, routine=routine)


@bp.get("/mis-rutinas/<int:routine_id>/")
@login_required
def personal_routine(routine_id):
    from app.services.movement import routine_done_today

    routine = owned_routine(current_user, routine_id)
    if routine is None:
        abort(404)
    return render_template(
        "wellness/personal_detail.html",
        routine=routine,
        visuals=VISUALS,
        completed=routine_done_today(current_user, routine.slug),
    )


@bp.post("/mis-rutinas/<int:routine_id>/archivar")
@login_required
@limiter.limit("30 per minute")
def archive_routine(routine_id):
    if not EmptyForm().validate_on_submit():
        abort(400)
    if not archive_personal_routine(current_user, routine_id):
        abort(404)
    flash("Rutina archivada. Tus actividades registradas y puntos se conservan.", "info")
    return redirect(url_for("wellness.library"))


@bp.post("/mis-rutinas/<int:routine_id>/registrar")
@login_required
@limiter.limit("30 per minute")
def complete_personal_routine(routine_id):
    from app.services.movement import register_routine

    if not EmptyForm().validate_on_submit():
        abort(400)
    result = register_routine(current_user, f"personal-{routine_id}")
    if result is None:
        abort(404)
    message = (
        f"Rutina registrada. +{result['points']} XP por tu constancia."
        if result["points"]
        else "Actividad registrada sin duplicar los puntos de movimiento de hoy."
    )
    flash(message, "success" if result["created"] else "info")
    return redirect(url_for("wellness.personal_routine", routine_id=routine_id))
