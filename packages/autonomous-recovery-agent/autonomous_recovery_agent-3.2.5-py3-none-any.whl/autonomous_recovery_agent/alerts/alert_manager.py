class AlertManager:
    def __init__(self, email_alert=None, logger=None):
        self.email_alert = email_alert
        self.logger = logger

    def send(self, level: str, title: str, message: str):
        self.logger.info(f"🔔 ALERT [{level}] {title}")

        # INFO → no email
        if level == "INFO":
            return

        # WARNING & CRITICAL → email
        if level in ["WARNING", "CRITICAL"] and self.email_alert:
            self.email_alert.send(
                subject=f"[{level}] {title}",
                message=message
            )
