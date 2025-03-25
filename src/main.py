import flet as ft
from app_layout import AppLayout
from contact_manager import ContactManager
from helpers import Account
import getGoogleContacts as googleApp

class ContactHarmonyApp(AppLayout):
    def __init__(self, page: ft.Page):
        self.contactManager = ContactManager()
        self.page = page
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=48),
            leading_width=100,
            title=ft.Text("ContactHarmony",size=32, text_align="start"),
            center_title=False,
            toolbar_height=75,
            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_700,
            actions=[
                ft.Container(
                    content=ft.FilledTonalButton(
                        "Connect Account",
                        on_click=self.connect_account
                    ),
                    margin=ft.margin.only(left=50, right=25)
                )
            ],
        )
        self.page.appbar = self.appbar
        self.page.update()
        super().__init__(
            self,
            self.page,
            tight=True,
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
    
    def connect_account(self, e):
        def close_dlg(e):
            if fieldEmail.value == "" or fieldApplicationPassword.value == "":
                fieldEmail.error_text = "Please provide Gmail Address"
                fieldApplicationPassword.error_text = "Please provide password"
                self.page.update()
                return
            else:
                # when info entered & button clicked, attempt to fetch contacts.
                #   on fail, do something. idk yet
                result = self.add_account("google", fieldEmail.value, fieldApplicationPassword.value)
                self.page.close(dialog)
                self.page.update()

        fieldEmail = ft.TextField(label="Gmail Address")
        fieldApplicationPassword = ft.TextField(label="Application Password", password=True)

        dialog = ft.AlertDialog(
            title=ft.Text("Please enter your Gmail address and application password"),
            content=ft.Column(
                [
                    fieldEmail,
                    fieldApplicationPassword,
                    ft.ElevatedButton(text="Connect", on_click=close_dlg),
                ],
                tight=True,
            )
        )
        self.page.open(dialog)

    def add_account(self, service, gmail, applicationPassword):
        # ContactManager's connect_account doesn't return anything so now this doesn't either
        newAccount = Account(service, gmail, applicationPassword)
        self.contactManager.connect_account(newAccount)
        return

if __name__ == "__main__":
 
    def main(page: ft.Page):
 
        page.title = "ContactHarmony"
        app = ContactHarmonyApp(page)
        page.add(app)
        page.update()
 
    ft.app(main)