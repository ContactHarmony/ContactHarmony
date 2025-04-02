import flet as ft
from contact_manager import ContactManager
from helpers import Account

class ContactPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
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
                        text = "Back",
                        icon = ft.Icons.ARROW_BACK,
                        on_click = lambda _ : self.unlookit()
                    ),
                    padding = 10
                )
            ]
        )
        self.controls = [ft.Container(
            height = 500,
            content = ft.ListView(
                controls = [],
                spacing = 2,
                divider_thickness = 2
            )
        )]
        self.populate_contacts()

    def unlookit(self):
        self.page.views.pop()
        self.page.update()
    
    def populate_contacts(self):
        # stub, will need to access contacts, iterate through them
        for i in range(20):
            self.controls[0].content.controls.append(ContactListTile("Demo McContactsson's Clone #%i" % (i)))
        self.page.update()

# temp build, bare minimum
class ContactListTile(ft.ListTile):
    def __init__(self, contactName):
        super().__init__()
        self.title = ft.Text(contactName)
        self.trailing = ft.FilledTonalButton(
            icon = ft.Icons.SEARCH,
            text = "View Contact"
        )