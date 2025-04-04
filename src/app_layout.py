import flet as ft

class AppLayout(ft.Row):
    def __init__(self, app, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page

        self.accountView: ft.Control = ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            ft.Text(
                                value="Your Backups",
                                theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                            ),
                            expand=True,
                            padding=ft.padding.only(top=15),
                        ),
                        ft.Container(
                            ft.FilledTonalButton(
                                "Connect Account",
                                icon=ft.Icons.ADD,
                                on_click=self.app.connect_account,
                            ),
                            padding=ft.padding.only(right=50, top=15),
                        )
                    ]
                ),
                ft.Row([ft.Text("No connected accounts")]),
            ]
        )

        self.contactListView: ft.Control = ft.Column()

        self.controls = [self.accountView]
        self.page.add(self.contactListView)


    def look_at(self, view):
        self.controls[0] = view
        self.page.update()

    def load_account_cards(self):
        self.accountView.controls[-1] = ft.Row(
            [
                ft.Card(
                    content = ft.Container(
                        content = ft.Column(
                            [
                                ft.Text(
                                    a.address,
                                    theme_style=ft.TextThemeStyle.LABEL_LARGE
                                ),
                                ft.Text(
                                    f"{a.service.title()} account"
                                ),
                                ft.Row(
                                    [
                                        ft.TextButton(
                                            "Browse Contacts",
                                            icon = ft.Icons.PERSON_SEARCH,
                                            icon_color = "blue200",
                                            tooltip = "Browse Contacts",
                                            on_click = lambda _ : self.look_at(self.make_contact_list_view(a))
                                        ),
                                        ft.IconButton(
                                            icon = ft.Icons.DELETE_FOREVER,
                                            icon_color = "pink500",
                                            tooltip = "Detach Account",
                                            on_click = lambda _ : self.app.remove_account(a)
                                        ),
                                    ],
                                    spacing = 10,
                                    alignment = ft.MainAxisAlignment.END
                                )
                            ],
                            spacing = 5
                        ),
                        padding = 10
                    ),
                    margin = 10,
                    width = 300
               )
                for a in self.app.contactManager.get_connected_accounts()
            ],
            wrap=True,
        )
        
    def make_contact_list_view(self, account):
        def make_contact_list_tiles():
            listTiles = []
            for c in self.app.get_contact_list(account):
                listTiles.append(
                    ft.ListTile(
                        title = ft.Text(c.full_name),
                        trailing = ft.IconButton(
                            icon = ft.Icons.SEARCH,
                            icon_color = "blue200",
                            tooltip = "View Contact",
                            on_click = lambda _, contact=c: self.view_contact(contact)
                        ),
                        on_click = lambda _, contact=c: self.view_contact(contact)
                    )
                )
            return listTiles
                            
        self.contactListView.controls = [
                ft.Row(
                    [
                        ft.Container(
                            ft.IconButton(
                                icon = ft.Icons.ARROW_CIRCLE_LEFT,
                                icon_color = "blue200",
                                tooltip = "Return to Account View",
                                on_click=lambda _: self.look_at(self.accountView),
                            )
                        ),
                        ft.Container(
                            ft.Text(
                                value = f"{account.address} Contacts",
                                theme_style = ft.TextThemeStyle.HEADLINE_SMALL,
                            ),
                        )
                    ]
                ),
                ft.Container(
                    height = 500,
                    content = ft.ListView(
                        make_contact_list_tiles(),
                        spacing = 2,
                        divider_thickness = 2,
                        expand=True
                    ),
                    expand=True
                )
            ]
        
        return self.contactListView
    
    def view_contact(self, contact):
        def close_dlg(e):
            self.page.close(dialog)

        def make_contact_body():
            body = [] 
            body.append(ContactLabel("Name"))
            body.append(ContactText(contact.full_name))
            for i, email in enumerate(contact.emails):
                body.append(ContactLabel(f"Email Address {i+1}"))
                if email.type != '':
                    body.append(ContactText(f"{email.email} ({email.type})"))
                else:
                    body.append(ContactText(f"{email.number}"))
            for i, phone in enumerate(contact.phones):
                body.append(ContactLabel(f"Phone Number {i+1}"))
                if phone.type != '':
                    body.append(ContactText(f"{phone.number} ({phone.type})"))
                else:
                    body.append(ContactText(f"{phone.number}"))
            body.append(ContactLabel("Date of Birth")),
            body.append(ContactText(contact.birthday)),
            body.append(ContactLabel("Organization")),
            body.append(ContactText(contact.organization[0]))
            body.append(ContactLabel("Title"))
            body.append(ContactText(contact.title))
            body.append(ContactLabel("Notes"))
            body.append(ContactText(contact.note))
            return body

        class ContactLabel(ft.Container):
            def __init__(self, text, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.content = ft.Text(
                    text,
                    theme_style = ft.TextThemeStyle.LABEL_SMALL
                )
                self.padding = ft.padding.only(top=13)
        
        class ContactText(ft.Text):
            def __init__(self, text, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.value = text
                self.theme_style = ft.TextThemeStyle.BODY_LARGE
        
        dialog = ft.AlertDialog(
            title = ft.Container(
                ft.CircleAvatar(
                    content = ft.Text("%s%s" % (contact.first_name[0], contact.last_name[0]), size = 30),
                    radius = 40
                ),
                alignment = ft.alignment.center
            ),
            content = ft.Column(
                make_contact_body(),
                spacing = 0
            )
        )
        self.page.open(dialog)