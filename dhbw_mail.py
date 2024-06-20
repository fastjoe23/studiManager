import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from config import Config


class DHBWMail:
    def __init__(self):
        config = Config()
        self.smtp_server = config.smtp_server
        self.smtp_port = config.smtp_port
        self.username = config.smtp_username
        self.password = config.smtp_password
        self.server = None
        # Logging
        self.logger = logging.getLogger("main")
        self.logger.debug("DHBW Mail called")

    def login(self):
        try:
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.server.starttls()
            self.logger.debug("Login to Email-Server")
            self.server.login(self.username, self.password)
            return True
        except Exception as e:
            self.logger.error("Error occurred: %s", e)
            return False

    """
    send_email_without_login
    Sends an email without logging in. This function constructs an email message and sends it using the provided SMTP server without performing an authentication step.
    Use it in loops, but don't forget to log in and log out before and afterwards.
    """
    def send_email_without_login(
        self, to_address, cc_address=None, subject="", body="", attachment_path=None
    ):
        result = {"success": False, "error_message": None}
        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = to_address
        msg["Cc"] = cc_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        if attachment_path:
            attachment = self._create_attachment(attachment_path)
            msg.attach(attachment)

        try:
            recipients = [to_address] + [cc_address] if cc_address else [to_address]
            self.server.sendmail(self.username, recipients, msg.as_string())
            result["success"] = True
            self.logger.debug(
                "Email mit Betreff '%s' an %s versendet", subject, recipients
            )
        except Exception as e:
            result["error_message"] = str(e)
            self.logger.error("Error occurred: %s", e)
        return result

    def logout(self):
        if self.server:
            self.logger.debug("Logout from Email-Server")
            self.server.quit()

    """
    send_email_with_login
    Sends an email with logging in. This function constructs an email message and sends it using the provided SMTP server without performing an authentication step.
    Use it for 1(!) email to send. Sending multiple mails with this function results in connections-rate-limits at the email-server.
    """
    def send_email_with_login(
        self, to_address, cc_address=None, subject="", body="", attachment_path=None
    ):
        result = {"success": False, "error_message": ""}
        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = to_address
        msg["Cc"] = cc_address
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        if attachment_path:
            attachment = self._create_attachment(attachment_path)
            msg.attach(attachment)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                recipients = [to_address] + [cc_address] if cc_address else [to_address]
                server.sendmail(self.username, recipients, msg.as_string())
                result["success"] = True
        except Exception as e:
            result["error_message"] = str(e)

        return result

    def _create_attachment(self, file_path):
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(open(file_path, "rb").read())
        encoders.encode_base64(attachment)
        attachment.add_header(
            "Content-Disposition", f'attachment; filename="{file_path}"'
        )
        return attachment
