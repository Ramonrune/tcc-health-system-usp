import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:

    sender_email = os.environ["EMAIL_SENDER"]
    app_password = os.environ["EMAIL_APP_PASSWORD"]

    def send_email(self, recipient_email: str, subject: str, html_content: str):

        print(recipient_email)
        print(subject)
        print(html_content)
        message = MIMEMultipart("alternative")
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.sender_email, self.app_password)
            server.sendmail(self.sender_email, recipient_email, message.as_string())
