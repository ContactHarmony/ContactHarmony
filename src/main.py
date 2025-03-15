import flet as ft
from app_layout import AppLayout

class ContactHarmonyApp(AppLayout):
    def __init__(self, page: ft.Page):
        self.page = page
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE),
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
                self.fetch_contacts(fieldEmail.value, fieldApplicationPassword.value)
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
            ),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.open(dialog)

    def fetch_contacts(self, gmail, applicationPassword):
        #TODO
        return True

if __name__ == "__main__":
 
    def main(page: ft.Page):
 
        page.title = "ContactHarmony"
        app = ContactHarmonyApp(page)
        page.add(app)
        page.update()
 
    ft.app(main)