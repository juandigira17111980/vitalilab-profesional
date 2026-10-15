from datetime import date

from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange, Regexp


def clean_name(value):
    return " ".join(value.split()) if value else value


class ManualSchoolJoinForm(FlaskForm):
    school_name = StringField(
        "Nombre de tu colegio",
        filters=[clean_name],
        validators=[DataRequired(), Length(min=3, max=160)],
    )
    group_name = StringField(
        "Grado, grupo o área",
        filters=[clean_name],
        validators=[DataRequired(), Length(min=1, max=80)],
    )
    requested_role = SelectField(
        "Mi rol solicitado",
        choices=[("student", "Estudiante"), ("teacher", "Docente")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Enviar mi solicitud")


class ManualEnrollmentReviewForm(FlaskForm):
    school_id = SelectField("Colegio verificado", coerce=int, validators=[InputRequired()])
    group_id = SelectField("Grupo verificado (obligatorio para estudiantes)", coerce=int, default=0)
    decision = SelectField(
        "Decisión", choices=[("approved", "Aprobar vinculación"), ("rejected", "No aprobar")]
    )
    verified = BooleanField(
        "He comprobado identidad, pertenencia y las autorizaciones aplicables, "
        "incluidas las del representante cuando corresponda."
    )
    submit = SubmitField("Guardar revisión")


class SchoolJoinForm(FlaskForm):
    school_id = SelectField("Colegio", coerce=int, validators=[InputRequired()])
    group_id = SelectField("Grupo (si está disponible)", coerce=int, default=0)
    requested_role = SelectField(
        "Mi rol solicitado",
        choices=[("student", "Estudiante"), ("teacher", "Docente")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Solicitar vinculación")


class SchoolForm(FlaskForm):
    name = StringField(
        "Nombre del colegio",
        filters=[lambda value: value.strip() if value else value],
        validators=[DataRequired(), Length(min=3, max=160)],
    )
    code = StringField(
        "Identificador (sin espacios)",
        filters=[lambda value: value.strip().lower() if value else value],
        validators=[DataRequired(), Length(max=60), Regexp(r"^[a-z0-9-]+$")],
    )
    submit = SubmitField("Crear colegio")


class SchoolGroupForm(FlaskForm):
    school_id = SelectField("Colegio", coerce=int, validators=[InputRequired()])
    name = StringField(
        "Nombre del grupo",
        filters=[lambda value: value.strip() if value else value],
        validators=[DataRequired(), Length(min=1, max=80)],
    )
    academic_year = IntegerField(
        "Año escolar",
        default=date.today().year,
        validators=[InputRequired(), NumberRange(min=2020, max=2100)],
    )
    submit = SubmitField("Crear grupo")


class ReviewMembershipForm(FlaskForm):
    group_id = SelectField("Grupo aprobado (obligatorio para estudiantes)", coerce=int, default=0)
    decision = SelectField(
        "Decisión",
        choices=[("approved", "Aprobar"), ("rejected", "Rechazar"), ("revoked", "Revocar")],
        validators=[DataRequired()],
    )
    verified = BooleanField(
        "He comprobado identidad, vínculo y autorizaciones aplicables, "
        "incluidas las del representante cuando corresponda."
    )
    submit = SubmitField("Guardar revisión")


class TeacherAssignmentForm(FlaskForm):
    membership_id = SelectField("Docente aprobado", coerce=int, validators=[InputRequired()])
    group_id = SelectField("Grupo a asignar", coerce=int, validators=[InputRequired()])
    submit = SubmitField("Asignar grupo")


class AggregateConsentForm(FlaskForm):
    allow_aggregate = BooleanField(
        "Quiero aportar mis registros nuevos a estadísticas agregadas del grupo. "
        "Es opcional y puedo retirarlo."
    )
    submit = SubmitField("Guardar preferencia")
