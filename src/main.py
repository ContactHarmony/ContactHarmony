import flet as ft

def main(page: ft.Page):
    page.title = "ContactHarmony"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    TEXT_SIZE = 16

    def connect_account_click(e):
        #TODO
        page.update()

    page.add(
        ft.Column(
            [
                ft.Text(value="No contacts backed-up. Connect an account to get started!",
                        size=TEXT_SIZE),
                ft.ElevatedButton("Connect Account", icon=ft.Icons.ADD, on_click=connect_account_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


ft.app(main)