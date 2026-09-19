# ==========================================
# DLSAU Alumni Tracking System
# utils/email_sender.py
# ==========================================

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import EMAIL, EMAIL_PASSWORD


def send_email(receiver, subject, body):

    message = MIMEMultipart()

    message["From"] = EMAIL
    message["To"] = receiver
    message["Subject"] = subject

    message.attach(
        MIMEText(body, "plain")
    )

    try:

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            EMAIL,
            EMAIL_PASSWORD
        )

        server.send_message(message)

        server.quit()

        return True

    except Exception as e:

        print(e)

        return False