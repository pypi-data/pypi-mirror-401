import smtplib
from email.message import EmailMessage
import logging
import os


class EmailAlert:
    def __init__(
        self,
        smtp_host="smtp.gmail.com",
        smtp_port=465,
        sender_email=None,
        sender_password=None,
        receiver_email=None,
        logger=None
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender_email = sender_email or os.getenv("ALERT_EMAIL")
        self.sender_password = sender_password or os.getenv("ALERT_EMAIL_PASSWORD")
        self.receiver_email = receiver_email or os.getenv("ALERT_RECEIVER_EMAIL")
        self.logger = logger or logging.getLogger(__name__)

    def send(self, subject: str, message: str):
        if not all([self.sender_email, self.sender_password, self.receiver_email]):
            self.logger.warning("📧 Email alert skipped: email config missing")
            return

        try:
            msg = EmailMessage()
            msg["From"] = self.sender_email
            msg["To"] = self.receiver_email
            msg["Subject"] = subject
            msg.set_content(message)

            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            self.logger.info("📧 Email alert sent successfully")

        except Exception as e:
            self.logger.error(f"❌ Failed to send email alert: {e}")
