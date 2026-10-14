import click
from email_validator import EmailNotValidError, validate_email
from flask.cli import with_appcontext

from app.extensions import db
from app.models import Habit, User, UserProfile

HABITS = (
    {
        "code": "hydration",
        "name": "Hidratación consciente",
        "description": "Completa tu meta personal de agua durante el día.",
        "category": "Nutrición",
        "icon": "💧",
        "points": 15,
        "sort_order": 10,
    },
    {
        "code": "active-break",
        "name": "Pausa activa",
        "description": "Muévete y estira durante al menos tres minutos.",
        "category": "Movimiento",
        "icon": "↗",
        "points": 15,
        "sort_order": 20,
    },
    {
        "code": "sleep",
        "name": "Descanso reparador",
        "description": "Prepara una rutina de descanso acorde con tu edad y tus necesidades.",
        "category": "Descanso",
        "icon": "☾",
        "points": 15,
        "sort_order": 30,
    },
    {
        "code": "mindful-minute",
        "name": "Minuto consciente",
        "description": "Haz una pausa de respiración consciente sin pantallas.",
        "category": "Bienestar",
        "icon": "◌",
        "points": 10,
        "sort_order": 40,
    },
    {
        "code": "screen-break",
        "name": "Pausa de pantallas",
        "description": "Desconéctate unos minutos y presta atención a tu entorno.",
        "category": "Enfoque",
        "icon": "☀",
        "points": 10,
        "sort_order": 50,
    },
    {
        "code": "daily-intention",
        "name": "Un día con intención",
        "description": "Elige una prioridad realista y da su primer paso.",
        "category": "Enfoque",
        "icon": "◎",
        "points": 10,
        "sort_order": 60,
    },
    {
        "code": "mindful-meal",
        "name": "Comida sin distracciones",
        "description": "Reserva un momento de tu comida para comer con calma, sin pantallas.",
        "category": "Nutrición",
        "icon": "◒",
        "points": 10,
        "sort_order": 70,
    },
    {
        "code": "gentle-movement",
        "name": "Movimiento a tu ritmo",
        "description": "Dedica un momento a una actividad suave que disfrutes y puedas realizar.",
        "category": "Movimiento",
        "icon": "↟",
        "points": 15,
        "sort_order": 80,
    },
)


def seed_habits() -> int:
    created = 0
    for values in HABITS:
        habit = db.session.scalar(db.select(Habit).where(Habit.code == values["code"]))
        if habit is None:
            db.session.add(Habit(**values))
            created += 1
        else:
            for key, value in values.items():
                setattr(habit, key, value)
            habit.active = True
    db.session.commit()
    return created


def register_commands(app) -> None:
    @app.cli.command("seed-habits")
    @with_appcontext
    def seed_habits_command():
        created = seed_habits()
        click.echo(f"Catálogo sincronizado. Hábitos nuevos: {created}")

    @app.cli.command("create-admin")
    @click.option("--email", prompt=True)
    @click.option("--name", prompt="Nombre visible")
    @click.password_option(confirmation_prompt=True)
    @with_appcontext
    def create_admin(email: str, name: str, password: str):
        try:
            normalized = validate_email(
                email.strip(), check_deliverability=False
            ).normalized.lower()
        except EmailNotValidError as error:
            raise click.ClickException("El correo no tiene un formato válido.") from error
        if (
            len(password) < 10
            or not any(character.isupper() for character in password)
            or not any(character.islower() for character in password)
            or not any(character.isdigit() for character in password)
        ):
            raise click.ClickException(
                "La contraseña debe tener 10 caracteres, mayúscula, minúscula y número."
            )
        if db.session.scalar(db.select(User).where(User.email == normalized)):
            raise click.ClickException("El correo ya existe.")
        user = User(email=normalized, role="admin")
        user.set_password(password)
        user.profile = UserProfile(display_name=name.strip())
        db.session.add(user)
        db.session.commit()
        click.echo("Administrador creado de forma segura.")
