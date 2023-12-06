from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_chat_confirmation_template(
    chat: dict,
    email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "МойДоктор. Подтверждение регистрации"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Подтвердите регистрацию</h1>
        """,
        subtype="html"
    )
    return email