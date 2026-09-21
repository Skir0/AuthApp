from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, NameEmail
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_verification_email(email: EmailStr, verify_url: str):
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
        <h2>Добро пожаловать!</h2>
        <p>Для завершения регистрации и подтверждения вашего email-адреса, пожалуйста, перейдите по ссылке ниже:</p>
        <div style="text-align: center; margin: 20px 0;">
            <a href="{verify_url}" style="background-color: #4CAF50; color: white; padding: 14px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px;">
                Подтвердить Email
            </a>
        </div>
        <p style="color: #555; font-size: 12px;">Если кнопка не работает, скопируйте и вставьте эту ссылку в браузер:</p>
        <p style="color: #555; font-size: 12px;">{verify_url}</p>
        <hr>
        <p style="font-size: 12px; color: #888;">Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо.</p>
    </div>
    """

    message = MessageSchema(
        subject="Подтверждение регистрации",
        recipients=[NameEmail("", email)],
        body=html_content,
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    await fm.send_message(message)