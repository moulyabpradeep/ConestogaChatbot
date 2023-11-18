import smtplib
import random
import string
from email.message import EmailMessage
def generate_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_email(receiver_email, code):
    sender_email = 'joel.mendonsa30@gmail.com'  
    sender_password = 'pkhymedcjtuwnied'  # Your generated App Password
    
    subject = "Two Factor Authorization Code"
    body = f"This is your Two Factor Authoriation code. Do not share it with anyone.\nYour Code is: {code}"

    message = EmailMessage()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(message)


verification_code = generate_code()
#send_email(user_email, verification_code)
