from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from app.admin.routes import admin_required
from app.extensions import db, limiter
from app.forms import EmptyForm
from app.models import (
    School,
    SchoolEnrollmentRequest,
    SchoolGroup,
    SchoolMembership,
    TeacherGroupAssignment,
)
from app.school.forms import (
    AggregateConsentForm,
    ManualEnrollmentReviewForm,
    ManualSchoolJoinForm,
    ReviewMembershipForm,
    SchoolForm,
    SchoolGroupForm,
    SchoolJoinForm,
    TeacherAssignmentForm,
)
from app.services.audit import record_event
from app.services.enrollment import (
    cancel_manual_enrollment,
    enrollment_for,
    request_manual_enrollment,
    review_manual_enrollment,
)
from app.services.school import (
    assign_teacher,
    configure_join_form,
    membership_for,
    report_for_group,
    request_membership,
    review_membership,
    school_choices,
    set_aggregate_consent,
    teacher_groups,
    teacher_membership,
    withdraw_membership,
)
from app.wellness.catalog import ROUTINES

bp = Blueprint("school", __name__)


@bp.route("/colegios/", methods=["GET", "POST"])
@login_required
@limiter.limit("20 per hour", methods=["POST"])
def account():
    # Compatibility for previously opened forms; new UI always uses manual input.
    legacy = (
        request.method == "POST"
        and "school_id" in request.form
        and "school_name" not in request.form
    )
    form = SchoolJoinForm() if legacy else ManualSchoolJoinForm()
    if legacy:
        configure_join_form(form)
    if form.validate_on_submit():
        try:
            if legacy:
                request_membership(
                    current_user, form.school_id.data, form.group_id.data, form.requested_role.data
                )
            else:
                request_manual_enrollment(
                    current_user,
                    form.school_name.data,
                    form.group_name.data,
                    form.requested_role.data,
                )
        except ValueError as error:
            flash(str(error), "error")
        else:
            flash(
                "Solicitud enviada. La revisión del vínculo y del rol es obligatoria "
                "antes de habilitar acceso escolar.",
                "success",
            )
            return redirect(url_for("school.account"))
    elif form.is_submitted():
        flash("Revisa el colegio, el grupo y el rol solicitado.", "error")
    if legacy:
        form = ManualSchoolJoinForm(formdata=None)
    member = membership_for(current_user)
    consent = AggregateConsentForm(allow_aggregate=member.allow_aggregate if member else False)
    return render_template(
        "school/account.html",
        form=form,
        member=member,
        consent=consent,
        action_form=EmptyForm(),
        enrollment=enrollment_for(current_user),
    )


@bp.post("/colegios/retirar")
@login_required
def withdraw():
    if not EmptyForm().validate_on_submit():
        abort(400)
    withdraw_membership(current_user)
    cancel_manual_enrollment(current_user)
    flash(
        "Vinculación retirada. Tus datos personales e historial se conservan "
        "y ya no aportan al reporte del grupo.",
        "info",
    )
    return redirect(url_for("school.account"))


@bp.post("/colegios/estadisticas")
@login_required
def consent():
    form = AggregateConsentForm()
    if not form.validate_on_submit():
        abort(400)
    try:
        set_aggregate_consent(current_user, form.allow_aggregate.data)
    except ValueError as error:
        flash(str(error), "error")
    else:
        flash(
            "Preferencia actualizada. Solo se consideran registros posteriores "
            "a la aprobación y a la activación del aporte.",
            "success",
        )
    return redirect(url_for("school.account"))


@bp.get("/docentes/")
@login_required
def teacher():
    member = teacher_membership(current_user)
    if member is None:
        abort(403)
    return render_template(
        "school/teacher.html", member=member, groups=teacher_groups(current_user), routines=ROUTINES
    )


@bp.get("/docentes/grupos/<int:group_id>")
@login_required
def group_report(group_id):
    try:
        report = report_for_group(current_user, group_id)
    except PermissionError:
        abort(404)
    record_event("school.aggregate_viewed", "school_group", group_id, current_user.id)
    db.session.commit()
    return render_template("school/report.html", report=report)


@bp.get("/docentes/rutinas/<slug>/proyectar")
@login_required
def project_routine(slug):
    if teacher_membership(current_user) is None:
        abort(403)
    routine = next((item for item in ROUTINES if item["slug"] == slug), None)
    if not routine:
        abort(404)
    return render_template("school/project.html", routine=routine)


def _admin_context():
    schools, groups = school_choices()
    group_form = SchoolGroupForm(prefix="group")
    group_form.school_id.choices = [(school.id, school.name) for school in schools]
    assignment_form = TeacherAssignmentForm(prefix="assignment")
    approved = list(
        db.session.scalars(
            db.select(SchoolMembership)
            .where(
                SchoolMembership.status == "approved", SchoolMembership.requested_role == "teacher"
            )
            .order_by(SchoolMembership.id)
        )
    )
    assignment_form.membership_id.choices = [
        (member.id, f"{member.user.profile.display_name} · {member.school.name}")
        for member in approved
    ]
    assignment_form.group_id.choices = [
        (group.id, f"{group.school.name} · {group.name} · {group.academic_year}")
        for group in groups
    ]
    return group_form, assignment_form


@bp.get("/admin/colegios/")
@admin_required
def admin_index():
    group_form, assignment_form = _admin_context()
    return render_template(
        "school/admin.html",
        school_form=SchoolForm(prefix="school"),
        group_form=group_form,
        assignment_form=assignment_form,
        schools=list(db.session.scalars(db.select(School).order_by(School.name))),
        groups=list(
            db.session.scalars(
                db.select(SchoolGroup).order_by(SchoolGroup.academic_year.desc(), SchoolGroup.name)
            )
        ),
        members=db.paginate(
            db.select(SchoolMembership).order_by(SchoolMembership.updated_at.desc()),
            per_page=20,
            error_out=False,
        ),
        assignments=list(db.session.scalars(db.select(TeacherGroupAssignment))),
        action_form=EmptyForm(),
        enrollments=db.paginate(
            db.select(SchoolEnrollmentRequest)
            .where(SchoolEnrollmentRequest.status == "pending")
            .order_by(SchoolEnrollmentRequest.created_at),
            page=request.args.get("requests_page", 1, type=int),
            per_page=20,
            error_out=False,
        ),
    )


@bp.route("/admin/colegios/altas/<int:request_id>", methods=["GET", "POST"])
@admin_required
def review_enrollment(request_id):
    if request_id > 2_147_483_647:
        abort(404)
    item = db.get_or_404(SchoolEnrollmentRequest, request_id)
    form = ManualEnrollmentReviewForm()
    schools, groups = school_choices()
    form.school_id.choices = [(0, "Elegir colegio verificado")] + [
        (school.id, school.name) for school in schools
    ]
    form.group_id.choices = [(0, "Sin grupo")] + [
        (group.id, f"{group.school.name} · {group.name} · {group.academic_year}")
        for group in groups
    ]
    if form.validate_on_submit():
        try:
            review_manual_enrollment(
                current_user,
                item.id,
                form.school_id.data,
                form.group_id.data,
                form.decision.data,
                form.verified.data,
            )
        except ValueError as error:
            flash(str(error), "error")
        else:
            flash(
                "Revisión guardada. Asigna grupos por separado si se trata de un docente.",
                "success",
            )
            return redirect(url_for("school.admin_index"))
    return render_template("school/review_enrollment.html", enrollment=item, form=form)


@bp.post("/admin/colegios/crear")
@admin_required
def create_school():
    form = SchoolForm(prefix="school")
    if form.validate_on_submit():
        school = School(code=form.code.data, name=form.name.data)
        db.session.add(school)
        try:
            db.session.flush()
            record_event("school.created", "school", school.id, current_user.id)
            db.session.commit()
            flash("Colegio creado.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Ese identificador ya está registrado.", "error")
    else:
        flash("Revisa el nombre y el identificador del colegio.", "error")
    return redirect(url_for("school.admin_index"))


@bp.post("/admin/colegios/grupos")
@admin_required
def create_group():
    form, _ = _admin_context()
    if form.validate_on_submit():
        group = SchoolGroup(
            school_id=form.school_id.data,
            name=form.name.data,
            academic_year=form.academic_year.data,
        )
        db.session.add(group)
        try:
            db.session.flush()
            record_event("school.group_created", "school_group", group.id, current_user.id)
            db.session.commit()
            flash("Grupo creado.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Ya existe ese grupo en el colegio y año escolar.", "error")
    else:
        flash("Revisa el colegio, nombre y año escolar.", "error")
    return redirect(url_for("school.admin_index"))


@bp.route("/admin/colegios/solicitudes/<int:membership_id>", methods=["GET", "POST"])
@admin_required
def review(membership_id):
    member = db.get_or_404(SchoolMembership, membership_id)
    form = ReviewMembershipForm()
    form.group_id.choices = [(0, "Sin grupo")] + [
        (group.id, f"{group.name} · {group.academic_year}")
        for group in db.session.scalars(
            db.select(SchoolGroup).where(
                SchoolGroup.school_id == member.school_id, SchoolGroup.active.is_(True)
            )
        )
    ]
    if form.validate_on_submit():
        try:
            review_membership(
                current_user, member.id, form.decision.data, form.group_id.data, form.verified.data
            )
        except ValueError as error:
            flash(str(error), "error")
        else:
            flash("Revisión guardada. Los permisos se comprueban en cada acceso.", "success")
            return redirect(url_for("school.admin_index"))
    elif not form.is_submitted():
        form.group_id.data = member.group_id or 0
    return render_template("school/review.html", member=member, form=form)


@bp.post("/admin/colegios/asignaciones")
@admin_required
def assign():
    _, form = _admin_context()
    if form.validate_on_submit():
        try:
            created = assign_teacher(current_user, form.membership_id.data, form.group_id.data)
        except ValueError as error:
            flash(str(error), "error")
        else:
            flash("Grupo asignado." if created else "La asignación ya existe.", "success")
    else:
        flash("Selecciona un docente aprobado y un grupo válido.", "error")
    return redirect(url_for("school.admin_index"))


@bp.post("/admin/colegios/asignaciones/<int:assignment_id>/retirar")
@admin_required
def remove_assignment(assignment_id):
    if not EmptyForm().validate_on_submit():
        abort(400)
    assignment = db.get_or_404(TeacherGroupAssignment, assignment_id)
    record_event(
        "school.assignment_removed",
        "school_group",
        assignment.group_id,
        current_user.id,
        {"assignment_id": assignment.id},
    )
    db.session.delete(assignment)
    db.session.commit()
    flash("Asignación retirada.", "info")
    return redirect(url_for("school.admin_index"))


@bp.post("/admin/colegios/<kind>/<int:item_id>/estado")
@admin_required
def toggle_status(kind, item_id):
    if not EmptyForm().validate_on_submit() or kind not in {"colegio", "grupo"}:
        abort(400)
    item = db.get_or_404(School if kind == "colegio" else SchoolGroup, item_id)
    item.active = not item.active
    record_event("school.status_changed", kind, item.id, current_user.id, {"active": item.active})
    db.session.commit()
    flash("Estado actualizado. Al pausar se interrumpe el acceso docente correspondiente.", "info")
    return redirect(url_for("school.admin_index"))
