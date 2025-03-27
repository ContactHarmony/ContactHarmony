import flet as ft

class AppLayout(ft.Row):
    def __init__(self, app, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self._active_view: ft.Control = ft.Column(
            #controls=[ft.Text("Active View")],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.page.add(
            ft.Card(
                content = ft.Container(
                    content = ft.Column(
                        [
                            ft.Markdown("""### Google
exampleaddress@gmail.com"""),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon = ft.Icons.DELETE_FOREVER,
                                        icon_color = "pink500",
                                        icon_size = 25,
                                        tooltip = "Detach Account"
                                    ),
                                    ft.IconButton(
                                        icon = ft.Icons.PERSON_SEARCH,
                                        icon_color = "blue200",
                                        icon_size = 25,
                                        tooltip = "View Contacts"
                                    ),
                                ],
                                spacing = 10,
                                alignment = ft.MainAxisAlignment.END
                            )
                        ],
                        spacing = 0
                    ),
                    padding = 10
                ),
                margin = 10,
                width = 250
            )
        )
        self.page.add(
            ft.Card(
                content = ft.Container(
                    ft.Row(
                        [
                            ft.Markdown("""### Google
exampleaddress@gmail.com"""),
                            ft.IconButton(
                                icon = ft.Icons.DELETE_FOREVER,
                                icon_color = "pink500",
                                icon_size = 25,
                                tooltip = "Detach Account"
                            ),
                            ft.IconButton(
                                icon = ft.Icons.PERSON_SEARCH,
                                icon_color = "blue200",
                                icon_size = 25,
                                tooltip = "View Contacts"
                            ),
                        ],
                        spacing = 10,
                        alignment = ft.MainAxisAlignment.START
                    ),
                    padding = 10
                ),
                margin = 10,
                width = 335
            )
        )
        self.page.add(
            ft.Card(
                content = ft.Container(
                    content = ft.Column(
                        [
                            ft.Markdown("""### Google
exampleaddress@gmail.com"""),
                            ft.Row(
                                [
                                    ft.OutlinedButton(text="Detach Account"),
                                    ft.OutlinedButton(text="View Contacts")
                                ],
                                spacing = 10,
                                alignment = ft.MainAxisAlignment.END
                            )
                        ]
                    ),
                    padding = 10
                ),
                margin = 10,
                width = 400
            )
        )
        self.controls = [self.active_view]

    @property
    def active_view(self):
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.update()

    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.page.update()
