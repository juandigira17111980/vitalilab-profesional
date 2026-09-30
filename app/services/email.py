import smtplib
from email.message import EmailMessage

from flask import current_app


def send_password_reset(recipient: str, reset_url: str) -> bool:
    config = current_app.config
    if not all(
        [config["MAIL_HOST"], config["MAIL_USERNAME"], config["MAIL_PASSWORD"], config["MAIL_FROM"]]
    ):
        current_app.logger.warning("Password reset requested but email is not configured")
        return False

    message = EmailMessage()
    message["Subject"] = "Restablece tu acceso a VitaliLab"
    message["From"] = config["MAIL_FROM"]
    message["To"] = recipient
    message.set_content(
        "Recibimos una solicitud para cambiar tu contraseña. "
        f"Abre este enlace durante la próxima hora: {reset_url}\n\n"
        "Si no solicitaste el cambio, ignora este mensaje."
    )
    with smtplib.SMTP(config["MAIL_HOST"], config["MAIL_PORT"], timeout=10) as server:
        if config["MAIL_USE_TLS"]:
            server.starttls()
        server.login(config["MAIL_USERNAME"], config["MAIL_PASSWORD"])
        server.send_message(message)
    return True
