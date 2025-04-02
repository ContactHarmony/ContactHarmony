import flet as ft
from contact_page import ContactListPage

class AppLayout(ft.Row):
    def __init__(self, app, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self._active_view: ft.Control = ft.Column(
            controls=[ft.Text("Active View")],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.account_view: ft.Control = ft.Column(
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

        self.controls = [self.account_view]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.update()

    def set_account_view(self):
        self.active_view = self.account_view
    
    def lookit_contacts(self):
        self.page.views.append(ContactListPage(self.page))
        self.page.update()

    def load_account_cards(self):
        self.account_view.controls[-1] = ft.Row(
            [
                ft.Card(
                    content = ft.Container(
                        content = ft.Column(
                            [
                                ft.Text(
                                    a.service.title(),
                                    theme_style=ft.TextThemeStyle.HEADLINE_SMALL
                                ),
                                ft.Text(
                                    a.address
                                ),
                                ft.Row(
                                    [
                                        ft.TextButton(
                                            "Browse Contacts",
                                            icon = ft.Icons.PERSON_SEARCH,
                                            icon_color = "blue200",
                                            tooltip = "Browse Contacts",
                                            on_click = lambda _ : self.lookit_contacts()
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
