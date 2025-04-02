import flet as ft
from contact_manager import ContactManager
from helpers import Account

class ContactListPage(ft.View):
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
            self.controls[0].content.controls.append(ContactListTile("Demo McContactsson's Clone #%i" % (i), self.page))
        self.page.update()

# temp build, bare minimum
class ContactListTile(ft.ListTile):
    def __init__(self, contactName, page):
        super().__init__()
        self.page = page
        self.title = ft.Text(contactName)
        self.trailing = ft.FilledTonalButton(
            icon = ft.Icons.SEARCH,
            text = "View Contact",
            on_click = lambda _ : self.view_contact()
        )

    def view_contact(self):
        self.page.views.append(ContactPage(self.page))
        self.page.update()

class ContactPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.controls = [
            ft.Container(
                content = ft.FilledTonalButton(
                    text = "Back",
                    icon = ft.Icons.ARROW_BACK,
                    on_click = lambda _ : self.unlookit()
                ),
                padding = 10,
                alignment = ft.alignment.top_right
            ),
            ft.Container(
                ft.Column(controls = [
                    ft.Container(
                        ft.CircleAvatar(
                            content = ft.Text("DT", size = 30),
                            radius = 40
                        ),
                        alignment = ft.alignment.center
                    ),
                    ft.Container(
                        content = ft.Column(controls = [
                            LabelS("\nName"),
                            BodyL("DemoText"),
                            LabelS("\nEmail Address"),
                            BodyL("DemoText"),
                            LabelS("\nPhone Number"),
                            BodyL("DemoText"),
                            LabelS("\nDate of Birth"),
                            BodyL("DemoText"),
                            LabelS("\nNotes"),
                            BodyL("DemoText")
                        ]),
                        alignment = ft.Alignment(-0.7,0)
                    )
                ]),
                padding = 10
            )
        ]

    def unlookit(self):
        self.page.views.pop()
        self.page.update()

class LabelS(ft.Text):
    def __init__(self, input):
        super().__init__()
        self.value = input
        self.theme_style = ft.TextThemeStyle.LABEL_SMALL

class BodyL(ft.Text):
    def __init__(self, input):
        super().__init__()
        self.value = input
        self.theme_style = ft.TextThemeStyle.BODY_LARGE