from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    DecimalField,
    EmailField,
    PasswordField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    InputRequired,
    Length,
    NumberRange,
    Optional,
    ValidationError,
)


def strong_password(_form, field) -> None:
    value = field.data or ""
    if len(value) < 10:
        raise ValidationError("Usa al menos 10 caracteres.")
    if not any(character.isupper() for character in value):
        raise ValidationError("Incluye al menos una letra mayúscula.")
    if not any(character.islower() for character in value):
        raise ValidationError("Incluye al menos una letra minúscula.")
    if not any(character.isdigit() for character in value):
        raise ValidationError("Incluye al menos un número.")


def normalize_email(value: str | None) -> str | None:
    """Normalize harmless whitespace and casing before email validation."""
    return value.strip().lower() if value else value


class RegisterForm(FlaskForm):
    display_name = StringField("Nombre o apodo", validators=[DataRequired(), Length(min=2, max=80)])
    email = EmailField(
        "Correo electrónico",
        filters=[normalize_email],
        validators=[DataRequired(), Email(), Length(max=254)],
    )
    password = PasswordField("Contraseña", validators=[InputRequired(), strong_password])
    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[InputRequired(), EqualTo("password", message="Las contraseñas no coinciden.")],
    )
    privacy_accepted = BooleanField(
        "Acepto la política de privacidad y el uso educativo de mis datos.",
        validators=[DataRequired(message="Debes aceptar la política para crear la cuenta.")],
    )
    submit = SubmitField("Crear mi cuenta")


class LoginForm(FlaskForm):
    email = EmailField(
        "Correo electrónico",
        filters=[normalize_email],
        validators=[DataRequired(), Email(), Length(max=254)],
    )
    password = PasswordField("Contraseña", validators=[InputRequired()])
    remember = BooleanField("Mantener mi sesión")
    submit = SubmitField("Ingresar")


class ForgotPasswordForm(FlaskForm):
    email = EmailField(
        "Correo electrónico",
        filters=[normalize_email],
        validators=[DataRequired(), Email(), Length(max=254)],
    )
    submit = SubmitField("Enviar instrucciones")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Nueva contraseña", validators=[InputRequired(), strong_password])
    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[InputRequired(), EqualTo("password", message="Las contraseñas no coinciden.")],
    )
    submit = SubmitField("Actualizar contraseña")


class ProfileForm(FlaskForm):
    display_name = StringField("Nombre o apodo", validators=[DataRequired(), Length(min=2, max=80)])
    birth_date = DateField("Fecha de nacimiento", validators=[Optional()])
    usage_mode = RadioField(
        "¿Cómo quieres usar VitaliLab?",
        choices=[("personal", "Uso personal"), ("institutional", "Uso institucional")],
        default="personal",
        validators=[DataRequired(message="Elige cómo quieres usar VitaliLab.")],
    )
    institution_name = StringField(
        "Institución (opcional)",
        filters=[lambda value: value.strip() if value else value],
        validators=[Optional(), Length(max=160)],
    )
    grade = StringField(
        "Grado, grupo o área (opcional)",
        filters=[lambda value: value.strip() if value else value],
        validators=[Optional(), Length(max=80)],
    )
    weight_kg = DecimalField(
        "Peso actual (kg)", validators=[Optional(), NumberRange(min=20, max=500)], places=2
    )
    height_cm = DecimalField(
        "Altura actual (cm)", validators=[Optional(), NumberRange(min=80, max=250)], places=2
    )
    submit = SubmitField("Guardar cambios")

    def validate_birth_date(self, field) -> None:
        if field.data and field.data > date.today():
            raise ValidationError("La fecha no puede estar en el futuro.")

    def validate_height_cm(self, field) -> None:
        if field.data and not self.weight_kg.data:
            raise ValidationError("Ingresa peso y altura juntos para calcular el IMC.")

    def validate_weight_kg(self, field) -> None:
        if field.data and not self.height_cm.data:
            raise ValidationError("Ingresa peso y altura juntos para calcular el IMC.")


class HabitCompletionForm(FlaskForm):
    submit = SubmitField("Marcar como cumplido")


class AnnouncementForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired(), Length(min=4, max=150)])
    body = TextAreaField("Contenido", validators=[DataRequired(), Length(min=10, max=3000)])
    submit = SubmitField("Guardar borrador")


class EmptyForm(FlaskForm):
    submit = SubmitField("Confirmar")


class GoalForm(FlaskForm):
    habit_id = SelectField(
        "¿Qué hábito quieres priorizar?", coerce=int, validators=[InputRequired()]
    )
    target_days = SelectField(
        "Tu meta en siete días",
        coerce=int,
        choices=[
            (number, f"{number} {'día' if number == 1 else 'días'}") for number in range(1, 8)
        ],
        validators=[InputRequired(), NumberRange(min=1, max=7)],
        default=3,
    )
    submit = SubmitField("Guardar mi meta")


class CheckInForm(FlaskForm):
    energy = SelectField(
        "¿Cómo sientes tu energía hoy?",
        coerce=int,
        choices=[
            (1, "1 · Muy baja"),
            (2, "2 · Baja"),
            (3, "3 · Media"),
            (4, "4 · Alta"),
            (5, "5 · Muy alta"),
        ],
        validators=[InputRequired(), NumberRange(min=1, max=5)],
    )
    focus = SelectField(
        "¿Cómo sientes tu capacidad de enfocarte?",
        coerce=int,
        choices=[
            (1, "1 · Muy baja"),
            (2, "2 · Baja"),
            (3, "3 · Media"),
            (4, "4 · Alta"),
            (5, "5 · Muy alta"),
        ],
        validators=[InputRequired(), NumberRange(min=1, max=5)],
    )
    submit = SubmitField("Guardar mi registro")
