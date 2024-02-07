import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from config import Config

class DHBWMail:
    def __init__(self):
        config = Config()
        self.smtpServer = config.smtpServer
        self.smtpPort = config.smtpPort
        self.username = config.smtpUsername
        self.password = config.smtpPassword

    def sendEmail(self, toAddress, ccAddress=None, subject='', body='', attachmentPath=None):
        result= {'success': False, 'errorMessage': ''}
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = toAddress
        msg['Cc'] = ccAddress
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachmentPath:
            attachment = self._createAttachment(attachmentPath)
            msg.attach(attachment)

        try:
            with smtplib.SMTP(self.smtpServer, self.smtpPort) as server:
                server.starttls()
                server.login(self.username, self.password)
                recipients = [toAddress] + [ccAddress] if ccAddress else [toAddress]
                server.sendmail(self.username, recipients, msg.as_string())
                result['success'] = True
        except Exception as e:
            result['errorMessage'] = str(e)
        
        return result

    def _createAttachment(self, file_path):
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(open(file_path, 'rb').read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename="{file_path}"')
        return attachment
