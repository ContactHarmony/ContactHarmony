import flet as ft
from app_views import HomeView, ContactsView
from contact_manager import ContactManager
from helpers import Account

# def ContactHarmonyApp(page: ft.Page):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.contactManager = ContactManager()

        

    #     self.appbar = ft.AppBar(
    #         leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=48),
    #         leading_width=100,
    #         title=ft.Text("Contact Harmony",size=32, text_align="start"),
    #         center_title=False,
    #         toolbar_height=75,
    #         bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_700,
    #         actions=[
    #             # ft.Container(
    #             #     content=ft.FilledTonalButton(
    #             #         "Connect Account",
    #             #         on_click=self.connect_account
    #             #     ),
    #             #     margin=ft.margin.only(left=50, right=25)
    #             # )
    #         ],
    #     )

    #     self.page.update()

    #     self.accountView: ft.Control = ft.Column(
    #         [
    #             ft.Row(
    #                 [
    #                     ft.Container(
    #                         ft.Text(
    #                             value="Your Backups",
    #                             theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
    #                         ),
    #                         expand=True,
    #                         padding=ft.padding.only(top=15),
    #                     ),
    #                     ft.Container(
    #                         ft.FilledTonalButton(
    #                             "Connect Account",
    #                             icon=ft.Icons.ADD,
    #                             on_click=self.app.connect_account,
    #                         ),
    #                         padding=ft.padding.only(right=50, top=15),
    #                     )
    #                 ]
    #             ),
    #             ft.Row([ft.Text("No connected accounts")]),
    #         ]
    #     )

    #     super().__init__(
    #         self,
    #         self.page,
    #         tight=True,
    #         expand=True,
    #         vertical_alignment=ft.CrossAxisAlignment.START,
    #     )

    # def open_view(self, view):
    #     self.page.views.append(view)
    #     self.page.update()

    # def load_account_cards(self):
    #     self.accountView.controls[-1] = ft.Row(
    #         [
    #             ft.Card(
    #                 content = ft.Container(
    #                     content = ft.Column(
    #                         [
    #                             ft.Text(
    #                                 a.address,
    #                                 theme_style=ft.TextThemeStyle.LABEL_LARGE
    #                             ),
    #                             ft.Text(
    #                                 f"{a.service.title()} account"
    #                             ),
    #                             ft.Row(
    #                                 [
    #                                     ft.TextButton(
    #                                         "Browse Contacts",
    #                                         icon = ft.Icons.PERSON_SEARCH,
    #                                         icon_color = "blue200",
    #                                         tooltip = "Browse Contacts",
    #                                         on_click = lambda _ : self.look_at(self.make_contact_list_view(a))
    #                                     ),
    #                                     ft.IconButton(
    #                                         icon = ft.Icons.DELETE_FOREVER,
    #                                         icon_color = "pink500",
    #                                         tooltip = "Detach Account",
    #                                         on_click = lambda _ : self.app.remove_account(a)
    #                                     ),
    #                                 ],
    #                                 spacing = 10,
    #                                 alignment = ft.MainAxisAlignment.END
    #                             )
    #                         ],
    #                         spacing = 5
    #                     ),
    #                     padding = 10
    #                 ),
    #                 margin = 10,
    #                 width = 300
    #            )
    #             for a in self.app.contactManager.get_connected_accounts()
    #         ],
    #         wrap=True,
    #     )
    
    # def connect_account(self, e):
    #     #TODO make it so you can choose type of account to connect
    #     def close_dlg(e):
    #         if fieldEmail.value == "" or fieldApplicationPassword.value == "":
    #             fieldEmail.error_text = "Please provide e-mail address"
    #             fieldApplicationPassword.error_text = "Please provide password"
    #             self.page.update()
    #             return
    #         else:
    #             # when info entered & button clicked, attempt to fetch contacts.
    #             #   on fail, do something. idk yet
    #             result = self.add_account(dropdownService.value, fieldEmail.value, fieldApplicationPassword.value)
    #             if result == True:
    #                 self.page.close(dialog)
    #                 self.load_account_cards()
    #                 self.page.update()
    #             else:
    #                 fieldEmail.error_text = "Error, failed to fetch contacts"
    #                 fieldApplicationPassword.error_text = "Try a different e-mail or password"
    #                 self.page.update()
    #                 return

    #     def get_service_options():
    #         options = []
    #         for service in self.contactManager.get_supported_services():
    #             options.append(
    #                 ft.DropdownOption(
    #                     key=service,
    #                     text=service.title(),
    #                 )
    #             )
    #         return options
        
    #     dropdownService = ft.Dropdown(
    #         editable=False,
    #         label="Service",
    #         options=get_service_options()
    #     )

    #     fieldEmail = ft.TextField(label="E-mail Address")
    #     fieldApplicationPassword = ft.TextField(label="Application Password", password=True)

    #     dialog = ft.AlertDialog(
    #         title=ft.Text("Please enter your e-mail address and application password"),
    #         content=ft.Column(
    #             [
    #                 dropdownService,
    #                 fieldEmail,
    #                 fieldApplicationPassword,
    #             ],
    #             tight=True,
    #         ),
    #         actions=[
    #             ft.ElevatedButton(text="Connect", on_click=close_dlg)
    #         ]
    #     )
    #     self.page.open(dialog)

    # def add_account(self, service, gmail, applicationPassword):
    #     # ContactManager's connect_account doesn't return anything so now this doesn't either
    #     newAccount = Account(service, gmail, applicationPassword)
    #     try:
    #         self.contactManager.connect_account(newAccount)
    #     except:
    #         return False
    #     else:
    #         return True
        
    # def remove_account(self, account):
    #     def close_dlg(e):
    #         self.page.close(dialog)
    #         if e.control.text != "No":
    #             self.contactManager.remove_account(account)
    #             self.load_account_cards()
    #         self.page.update()

    #     dialog = ft.AlertDialog(
    #         title=ft.Text("Removal Confirmation"),
    #         content=ft.Text(f"Are you sure you want to remove the backup for {account.service.title()} account {account.address}? This action cannot be undone."),
    #         actions=[
    #             ft.TextButton("No", on_click=close_dlg),
    #             ft.TextButton("Yes", on_click=close_dlg)
    #         ]
    #     )
    #     self.page.open(dialog)

    # def get_contact_list(self, account):
    #     try:
    #         contactList = self.contactManager.get_account_contacts(account)
    #     except:
    #         return None
    #     return contactList
        
    

if __name__ == "__main__":
 
    def contact_harmony_app(page: ft.Page):
        
        page.title = "Contact Harmony"
        page.update()
        contactManager = ContactManager()

        testAccount = Account("google", "contactharmony.test@gmail.com", "iham kmcq kjjb flxk")
        contactManager.connect_account(testAccount)

        def route_change(e):
            troute = ft.TemplateRoute(page.route)
            page.views.clear()
            page.views.append(HomeView(page, contactManager, route="/"))
            if troute.match("/contacts/:service/:address"):
                account = None
                for a in contactManager.get_connected_accounts():
                    if a.service == troute.service and a.address == troute.address:
                        account = a
                        break
                if account is None:
                    page.go("/")
                else:
                    page.views.append(ContactsView(page, contactManager, account, route=f"/contacts/{troute.service}/{troute.address}"))
            page.update()

        def view_pop(e):
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)

        page.views.append(HomeView(page, contactManager))
        page.update()
    
    ft.app(contact_harmony_app)