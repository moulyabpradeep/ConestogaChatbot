import flet as ft
from mailing import verification_code


def main(page):
    page.title = "TWO FACTOR AUTHENTICATION"
    def btn_click(e):
        if not code.value:
            code.error_text = "Please enter the Verification Code"
            page.update()
        else:
            if verification_code == str(code.value):
                page.clean()
                #page.add(ft.Text("Welcome to the chatbot"))
            elif verification_code != str(code.value): 
                code.error_text = 'Wrong code entered \nEnter the correct code'
                page.update()
    
    code = ft.TextField(label="Enter the Code")

    page.add(code, ft.ElevatedButton("Enter", on_click=btn_click))    

ft.app(target=main)
