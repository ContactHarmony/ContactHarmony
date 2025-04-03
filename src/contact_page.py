import flet as ft
from contact_manager import ContactManager
from helpers import Account
from VCFparser import VCF_parser, ContactPhone, ContactEmail, Contact

class ContactListPage(ft.View):
    def __init__(self, page: ft.Page, contactList):
        super().__init__()
        self.page = page
        self.contactList = contactList
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
        for i in range(len(self.contactList)):
            self.controls[0].content.controls.append(ContactListTile(self.contactList[i], self.page))
        #for i in range(20):
        #    self.controls[0].content.controls.append(ContactListTile("Demo McContactsson's Clone #%i" % (i), self.page))
        self.page.update()

# temp build, bare minimum
class ContactListTile(ft.ListTile):
    def __init__(self, parsedContact, page):
        super().__init__()
        self.page = page
        self.title = ft.Text(parsedContact.full_name)
        self.trailing = ft.FilledTonalButton(
            icon = ft.Icons.SEARCH,
            text = "View Contact",
            on_click = lambda _ : self.view_contact(parsedContact)
        )

    def view_contact(self, parsedContact):
        self.page.views.append(ContactPage(parsedContact, self.page))
        self.page.update()

class ContactPage(ft.View):
    def __init__(self, parsedContact, page: ft.Page):
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
                            content = ft.Text("%s%s" % (parsedContact.first_name[0], parsedContact.last_name[0]), size = 30),
                            radius = 40
                        ),
                        alignment = ft.alignment.center
                    ),
                    ft.Container(
                        content = ft.Column(
                            controls = [
                                LabelS("\nName"),
                                BodyL(parsedContact.full_name),
                                LabelS("\nEmail Address"),
                                BodyList(parsedContact.emails, "e"),
                                LabelS("\nPhone Number"),
                                BodyList(parsedContact.phones, "p"),
                                LabelS("\nDate of Birth"),
                                BodyL(parsedContact.birthday),
                                LabelS("\nOrganization"),
                                BodyL(parsedContact.organization),
                                LabelS("\nTitle"),
                                BodyL(parsedContact.title),
                                LabelS("\nNotes"),
                                BodyL(parsedContact.note),
                            ],
                            spacing = 0
                        ),
                        alignment = ft.Alignment(-0.7,0)
                    )],
                    spacing = 0
                ),
                padding = 10,
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

class BodyList(ft.Column):
    def __init__(self, input, type):
        super().__init__()
        if type == "e":
            for i in input:
                self.controls.append(BodyL(i.email))
        else:
            for i in input:
                self.controls.append(BodyL(i.number))

class BodyL(ft.Text):
    def __init__(self, input):
        super().__init__()
        self.value = input
        self.theme_style = ft.TextThemeStyle.BODY_LARGE