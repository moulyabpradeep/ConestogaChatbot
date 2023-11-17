import flet as ft
import smtplib
import random
import string
from email.message import EmailMessage
def generate_code(length=6):
    # Generate a random code of specified length
    return ''.join(random.choices(string.digits, k=length))

def send_email(receiver_email, code):
    sender_email = 'joel.mendonsa30@gmail.com'  # Your Gmail address
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

# Usage example:
user_email = 'joel.edwin05@gmail.com'  
verification_code = generate_code()
send_email(user_email, verification_code)

def main(page):
    def btn_click(e):
        if not code.value:
            code.error_text = "Please enter the Verification Code"
            page.update()
        else:
            if verification_code == str(code.value):
                page.clean()
                page.add(ft.Text("Welcome to the chatbot"))
            elif verification_code != str(code.value): 
                code.error_text = 'Wrong code entered \nEnter the correct code'
                page.update()
    
    code = ft.TextField(label="Enter the Code")

    page.add(code, ft.ElevatedButton("Enter", on_click=btn_click))    

ft.app(target=main)