import smtplib
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

    def send_email(self, to_address, cc_address=None, subject='', body='', attachment_path=None):
        result= {'success': False, 'error_message': ''}
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_address
        msg['Cc'] = cc_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachment_path:
            attachment = self._create_attachment(attachment_path)
            msg.attach(attachment)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                recipients = [to_address] + [cc_address] if cc_address else [to_address]
                server.sendmail(self.username, recipients, msg.as_string())
                result['success'] = True
        except Exception as e:
            result['error_message'] = str(e)

        return result

    def _create_attachment(self, file_path):
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(open(file_path, 'rb').read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename="{file_path}"')
        return attachment
