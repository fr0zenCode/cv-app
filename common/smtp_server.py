import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr

from common.security import generate_verification_code
from config import settings

def send_email_confirmation_code(receiver_email: EmailStr):
    verification_code = generate_verification_code()
    sender_email = settings.our_email


    message = MIMEMultipart("alternative")
    message["Subject"] = "CV Updater Email Verification"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"{verification_code}"

    env = Environment(loader=FileSystemLoader("../templates"))

    template = env.get_template("verification_email_template.html")
    html = template.render(verification_code=verification_code)

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)


    port = settings.SMTP_port
    password = settings.GMAIL_app_password

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(settings.SMTP_host, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, str(receiver_email), message.as_string())
