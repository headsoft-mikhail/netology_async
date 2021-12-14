from email.message import EmailMessage
import aiosmtplib
from config import HOST, PORT, USERNAME, PASSWORD

async def send_email( email, subject, text):
    message = EmailMessage()
    message["From"] = "Python developer"
    message["To"] = email
    message["Subject"] = subject
    message.set_content(text)
    # print(email, text)
    await aiosmtplib.send(message, hostname=HOST, port=PORT, username=USERNAME, password=PASSWORD)
