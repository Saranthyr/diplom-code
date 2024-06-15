from smtplib import SMTP
from email.message import EmailMessage


class MailerService:
    def __init__(self, sender: str, host: str, port: int, password: str) -> None:
        self.sender = sender
        self.sender_password = password
        self.host = host
        self.port = port

    async def send_mail(self, reciever: str, subject: str, content: str) -> int:
        message = EmailMessage()
        message["From"] = self.sender
        message["To"] = reciever
        message["Subject"] = subject
        message.set_content(content)
        client = SMTP(self.host, self.port)
        with client:
            client.login(self.sender, self.sender_password)
            client.send_message(message)
        return 0
