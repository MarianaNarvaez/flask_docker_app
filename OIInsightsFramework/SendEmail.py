from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import logging


class Email:
    def __init__(self,
                 sender_email: str,
                 receiver_email: str,
                 subject: str,
                 body: str,
                 isbody_html: bool = True,
                 host: str = "",
                 port: str = 25):
        self.sender_email: str = sender_email
        self.receiver_email: str = receiver_email
        self.body: str = body
        self.subject: str = subject
        self.isbody_html: bool = isbody_html
        self.host: str = host
        self.port: str = port

    def SendEmail(self):
        message: MIMEMultipart = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = self.sender_email
        message["To"] = (', ').join(
            self.receiver_email.split(',') if
            (',' in self.receiver_email) else self.receiver_email.split(';'))
        part = MIMEText(self.body, "html") if (self.isbody_html) else MIMEText(
            self.body, "plain")
        message.attach(part)
        logging.info(
            "Sending SMTP email using Host '{}' Port '{}'  \n 'Subject' : '{}' \n 'From' : '{}' \n 'To' : '{}' \n 'body' : '{}' "
            .format(self.host, self.port, self.subject, self.sender_email,
                    self.receiver_email, self.body))
        with smtplib.SMTP(self.host, self.port) as server:
            server.send_message(message)