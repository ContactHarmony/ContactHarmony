import flet as ft
from contact_manager import ContactManager
from helpers import Account

class ContactPage(ft.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=48),
            leading_width=100,
            title=ft.Text("Contact Search",size=32, text_align="start"),
            center_title=False,
            toolbar_height=75,
            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_700,
            actions = [
                ft.Container(
                    content = ft.FilledTonalButton(
                        "Back",
                        icon = ft.Icons.ARROW_BACK,
                        on_click = lambda _ : self.unlookit()
                    ),
                    padding = 10
                )
            ]
        )
        self.controls = []

    def unlookit(self):
        self.page.views.pop()
        self.page.update()