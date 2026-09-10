import asyncio
import logging
import smtplib
from email.message import EmailMessage
from typing import List

from app.config import get_settings

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self):
        self.settings = get_settings()

    def _email_configured(self) -> bool:
        return bool(self.settings.SMTP_HOST and self.settings.SMTP_USERNAME and self.settings.SMTP_PASSWORD)

    def _send_email_sync(self, recipient: str, subject: str, message: str) -> None:
        email = EmailMessage()
        email["From"] = self.settings.SMTP_FROM
        email["To"] = recipient
        email["Subject"] = subject
        email.set_content(message)
        with smtplib.SMTP(self.settings.SMTP_HOST, self.settings.SMTP_PORT, timeout=15) as client:
            client.starttls()
            client.login(self.settings.SMTP_USERNAME, self.settings.SMTP_PASSWORD)
            client.send_message(email)

    async def send_alert(self, channels: List[str], message: str, recipients: List[str]) -> None:
        if "email" not in channels:
            logger.info("Alert channels=%s recipients=%s message=%s", channels, recipients, message)
            return
        if not self._email_configured():
            logger.info("Email preview recipients=%s message=%s", recipients, message)
            return
        await asyncio.gather(*[
            asyncio.to_thread(self._send_email_sync, recipient, "BuildSure AI safety alert", message)
            for recipient in recipients
        ])

    async def send_registration_email(self, recipient: str, full_name: str) -> None:
        message = f"Hello {full_name},\n\nYour BuildSure AI account is ready. Sign in to monitor construction safety, compliance, and insurance risk.\n"
        await self.send_alert(["email"], message, [recipient])
