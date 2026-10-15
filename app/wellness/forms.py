from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    FieldList,
    Form,
    FormField,
    HiddenField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    NumberRange,
    Optional,
    ValidationError,
)

from app.forms import ProfileForm

GOAL_CHOICES = [
    ("center", "Postura y estabilidad"),
    ("energy", "Energía y movimiento"),
    ("strength", "Fuerza y tonificación"),
]
PREFERENCE_CHOICES = [
    ("adaptable", "Quiero explorar opciones adaptables"),
    ("seated", "Prefiero moverme sentado/a"),
    ("supported", "Prefiero apoyo de pared o silla"),
    ("standing", "Me siento cómodo/a de pie"),
]
VISUAL_CHOICES = [
    ("custom", "Mi ejercicio (sin demostración específica)"),
    ("posture", "Postura sentada"),
    ("march", "Movimiento alterno de brazos"),
    ("palms", "Presión de palmas"),
    ("shoulders", "Movilidad de hombros"),
    ("wall", "Apoyo en pared"),
    ("walk", "Pasos suaves"),
    ("breathing", "Pausa de respiración"),
]


def clean_text(value):
    return " ".join(value.split()) if value else value


class MeasurementSetupForm(ProfileForm):
    """Reuse measurement validators; unrelated profile fields are removed in __init__."""

    measurement_consent = BooleanField(
        "Quiero guardar estas mediciones para mi seguimiento personal.",
        validators=[DataRequired(message="Confirma si quieres guardar tus mediciones.")],
    )
    submit = SubmitField("Calcular y continuar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("display_name", "usage_mode", "institution_name", "grade", "movement_goal"):
            del self[name]
        self.weight_kg.validators = [InputRequired(), *self.weight_kg.validators[1:]]
        self.height_cm.validators = [InputRequired(), *self.height_cm.validators[1:]]


class MovementGoalForm(FlaskForm):
    movement_goal = SelectField("¿Qué quieres conseguir con tu rutina?", choices=GOAL_CHOICES)
    movement_preference = SelectField("¿Cómo prefieres moverte?", choices=PREFERENCE_CHOICES)
    submit = SubmitField("Guardar mi objetivo y ver rutinas")


class ExerciseForm(Form):
    name = StringField(
        "Nombre del ejercicio", filters=[clean_text], validators=[DataRequired(), Length(max=80)]
    )
    sets = IntegerField(
        "Series", default=1, validators=[InputRequired(), NumberRange(min=1, max=20)]
    )
    repetitions = IntegerField(
        "Repeticiones por serie", validators=[Optional(), NumberRange(min=1, max=200)]
    )
    duration_seconds = IntegerField(
        "Segundos por serie", validators=[Optional(), NumberRange(min=5, max=3600)]
    )
    rest_seconds = IntegerField(
        "Descanso entre series (segundos)",
        default=30,
        validators=[InputRequired(), NumberRange(min=0, max=600)],
    )
    visual = SelectField("Guía visual", choices=VISUAL_CHOICES, default="custom")
    instructions = TextAreaField(
        "Mis indicaciones", filters=[clean_text], validators=[Optional(), Length(max=280)]
    )

    def validate(self, extra_validators=None):
        valid = super().validate(extra_validators=extra_validators)
        # Optional stops field-level validators on blank input; this rule spans two fields.
        if self.repetitions.data is None and self.duration_seconds.data is None:
            self.duration_seconds.errors.append(
                "Indica repeticiones, segundos o ambos para este ejercicio."
            )
            valid = False
        return valid


class PersonalRoutineForm(FlaskForm):
    revision = HiddenField(default="0")
    name = StringField(
        "Nombre de mi rutina", filters=[clean_text], validators=[DataRequired(), Length(max=80)]
    )
    goal = SelectField("Objetivo de esta rutina", choices=GOAL_CHOICES)
    description = TextAreaField(
        "Descripción (opcional)", filters=[clean_text], validators=[Optional(), Length(max=500)]
    )
    exercises = FieldList(FormField(ExerciseForm), min_entries=1, max_entries=12)
    submit = SubmitField("Guardar mi rutina")

    def validate_revision(self, field):
        if not field.data or not field.data.isdigit() or len(field.data) > 10:
            raise ValidationError("Recarga el formulario antes de guardar.")

    def validate_exercises(self, field):
        # FieldList truncates excessive indices: reject rather than silently discard input.
        from flask import request

        indices = {
            key.split("-")[1]
            for key in request.form
            if key.startswith("exercises-") and len(key.split("-")) >= 3
        }
        if len(indices) > 12:
            raise ValidationError("Cada rutina admite hasta 12 ejercicios.")
