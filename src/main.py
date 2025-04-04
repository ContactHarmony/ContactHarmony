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
            title=ft.Text("Contact Harmony",size=32, text_align="start"),
            center_title=False,
            toolbar_height=75,
            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_700,
            actions=[
                # ft.Container(
                #     content=ft.FilledTonalButton(
                #         "Connect Account",
                #         on_click=self.connect_account
                #     ),
                #     margin=ft.margin.only(left=50, right=25)
                # )
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
        #TODO make it so you can choose type of account to connect
        def close_dlg(e):
            if fieldEmail.value == "" or fieldApplicationPassword.value == "":
                fieldEmail.error_text = "Please provide e-mail address"
                fieldApplicationPassword.error_text = "Please provide password"
                self.page.update()
                return
            else:
                # when info entered & button clicked, attempt to fetch contacts.
                #   on fail, do something. idk yet
                result = self.add_account(dropdownService.value, fieldEmail.value, fieldApplicationPassword.value)
                if result == True:
                    self.page.close(dialog)
                    self.load_account_cards()
                    self.page.update()
                else:
                    fieldEmail.error_text = "Error, failed to fetch contacts"
                    fieldApplicationPassword.error_text = "Try a different e-mail or password"
                    self.page.update()
                    return

        def get_service_options():
            options = []
            for service in self.contactManager.get_supported_services():
                options.append(
                    ft.DropdownOption(
                        key=service,
                        text=service.title(),
                    )
                )
            return options
        
        dropdownService = ft.Dropdown(
            editable=False,
            label="Service",
            options=get_service_options()
        )

        fieldEmail = ft.TextField(label="E-mail Address")
        fieldApplicationPassword = ft.TextField(label="Application Password", password=True)

        dialog = ft.AlertDialog(
            title=ft.Text("Please enter your e-mail address and application password"),
            content=ft.Column(
                [
                    dropdownService,
                    fieldEmail,
                    fieldApplicationPassword,
                ],
                tight=True,
            ),
            actions=[
                ft.ElevatedButton(text="Connect", on_click=close_dlg)
            ]
        )
        self.page.open(dialog)

    def add_account(self, service, gmail, applicationPassword):
        # ContactManager's connect_account doesn't return anything so now this doesn't either
        newAccount = Account(service, gmail, applicationPassword)
        try:
            self.contactManager.connect_account(newAccount)
        except:
            return False
        else:
            return True
        
    def remove_account(self, account):
        def close_dlg(e):
            self.page.close(dialog)
            if e.control.text != "No":
                self.contactManager.remove_account(account)
                self.load_account_cards()
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Removal Confirmation"),
            content=ft.Text(f"Are you sure you want to remove the backup for {account.service.title()} account {account.address}? This action cannot be undone."),
            actions=[
                ft.TextButton("No", on_click=close_dlg),
                ft.TextButton("Yes", on_click=close_dlg)
            ]
        )
        self.page.open(dialog)

    def get_contact_list(self, account):
        try:
            contactList = self.contactManager.get_account_contacts(account)
        except:
            return None
        return contactList
        
    

if __name__ == "__main__":
 
    def main(page: ft.Page):
 
        page.title = "ContactHarmony"
        app = ContactHarmonyApp(page)
        page.add(app)
        page.update()
 
    ft.app(main)