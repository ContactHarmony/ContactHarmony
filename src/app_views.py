import flet as ft
import os
from contact_manager import ContactManager
from helpers import Account, searchContacts, sortContacts

class HomeView(ft.View):
    def __init__(self, page: ft.Page, contactManager: ContactManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.contactManager = contactManager

        self.expand = True
        self.tight = True
        self.vertical_alignment = ft.MainAxisAlignment.START

        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=48),
            leading_width=100,
            title=ft.Text("Contact Harmony",size=32, text_align="start"),
            center_title=False,
            toolbar_height=75,
            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_700,
        )

        self.filePicker = ft.FilePicker(on_result=self.open_vcf)
        self.page.overlay.append(self.filePicker)

        self.controls = [
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
                            on_click=lambda _ : self.connect_account_dlg(),
                        ),
                        padding=ft.padding.only(top=15),
                    ),
                    ft.Container(
                        ft.FilledTonalButton(
                            "Open VCF",
                            icon=ft.Icons.INSERT_DRIVE_FILE,
                            on_click=lambda _ : self.filePicker.pick_files(allowed_extensions=["vcf"]),
                        ),
                        padding=ft.padding.only(right=50, top=15),
                    )
                ]
            ),
            ft.Row([ft.Text("No connected accounts")]),
        ]

        self.load_account_cards()

    def open_account_contact_page(self, account: Account):
        self.page.go(f"/contacts/{account.service}/{account.address}")

    def connect_account_dlg(self):
        def close_dlg(e):
            if fieldEmail.value == "" or fieldApplicationPassword.value == "" or dropdownService.value == "":
                dropdownService.error_text = "Please select a service"
                fieldEmail.error_text = "Please provide e-mail address"
                fieldApplicationPassword.error_text = "Please provide password"
                self.page.update()
            else:
                # when info entered & button clicked, attempt to fetch contacts.
                #   on fail, do something. idk yet
                result = self.contactManager.connect_account(Account(dropdownService.value, fieldEmail.value, fieldApplicationPassword.value))
                if result == True:
                    self.page.close(dialog)
                    self.load_account_cards()
                    self.page.update()
                else:
                    fieldEmail.error_text = "Error, failed to fetch contacts"
                    fieldApplicationPassword.error_text = "Try a different e-mail or password"
                    self.page.update()
                
        def get_service_options():
            options = []
            for service in self.contactManager.get_supported_services():
                options.append(
                    ft.DropdownOption(
                        key=service,
                        text=service.title(),
                    )
                )
            return options
        
        dropdownService = ft.Dropdown(
            editable=False,
            label="Service",
            options=get_service_options()
        )

        fieldEmail = ft.TextField(label="E-mail Address")
        fieldApplicationPassword = ft.TextField(label="Application Password", password=True)

        dialog = ft.AlertDialog(
            title=ft.Text("Please enter your e-mail address and application password"),
            content=ft.Column(
                [
                    dropdownService,
                    fieldEmail,
                    fieldApplicationPassword,
                ],
                tight=True,
            ),
            actions=[
                ft.ElevatedButton(text="Connect", on_click=close_dlg)
            ]
        )
        self.page.open(dialog)
    
    def remove_account_dlg(self, account: Account):
        def close_dlg(e):
            self.page.close(dialog)
            if e.control.text != "No":
                self.contactManager.remove_account(account)
                self.load_account_cards()
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Removal Confirmation"),
            content=ft.Text(f"Are you sure you want to remove the backup for {account.service.title()} account {account.address}? This action cannot be undone."),
            actions=[
                ft.TextButton("No", on_click=close_dlg),
                ft.TextButton("Yes", on_click=close_dlg)
            ]
        )
        self.page.open(dialog)

    def load_account_cards(self):
        if len(self.contactManager.get_connected_accounts()) == 0:
            self.controls[-1] = ft.Row([ft.Text("No connected accounts")])
        else:
            self.controls[-1] = ft.Row(
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
                                                on_click = lambda _, account=a : self.open_account_contact_page(account)
                                            ),
                                            ft.IconButton(
                                                icon = ft.Icons.DELETE_FOREVER,
                                                icon_color = "pink500",
                                                tooltip = "Detach Account",
                                                on_click = lambda _, account=a : self.remove_account_dlg(account)
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
                    for a in self.contactManager.get_connected_accounts()
                ],
                wrap=True,
            )
            self.page.update()

    def open_vcf(self, e):
        if e.files is not None:
            filePath = e.files[0].path
            self.contactManager.fileLook = filePath
            self.page.go("/file")
        

class ContactsView(ft.View):
    def __init__(self, page: ft.Page, contactManager: ContactManager, *args, **kwargs):
        super().__init__(*args, **kwargs,)
        self.page = page
        self.contactManager = contactManager

        self.expand = True
        self.tight = True
        self.vertical_alignment = ft.MainAxisAlignment.START
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.appbar = ft.AppBar(
            title=ft.Text(f"{self.get_title()} Contacts", text_align="start", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
            center_title=False,
            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_700
        )

        def on_search(e):
            if self.searchBar.value != "":      
                self.searchBar.bar_trailing = [ft.IconButton(
                    icon = ft.Icons.CLOSE,
                    # icon_color = "blue200",
                    tooltip = "Close Search",
                    on_click = close_search
                )]          
                self.load_contacts(searchTerm=self.searchBar.value)
            else:
                close_search()
        def close_search(e = None):
            self.load_contacts()
            self.searchBar.value = ""
            self.searchBar.bar_trailing.pop()
            self.searchBar.blur()
        self.searchBar = ft.SearchBar(
            full_screen=True,
            bar_hint_text="Search conacts...",
            view_hint_text="Search by name, email, phone number...",
            on_submit=on_search
            # on_tap=lambda _: self.searchBar.open_view()
        )
        

        self.controls = [
            self.searchBar,
            ft.Row([ft.Text("This account has no contacts")])
        ]

        self.contacts = []

        self.load_contacts()

    def add_contact_dlg(self, contact):
        def close_dlg(e):
            if dropdown_account.value is None:
                dropdown_account.error_text = "Please select an account"
                self.page.update()
            else:
                account_array = dropdown_account.value.split(',')
                selected_account = Account(account_array[0], account_array[1], account_array[2])
                if hasattr(self, 'account') and selected_account.address == self.account.address:
                    dropdown_account.error_text = "Please select a different account"
                    self.page.update()
                else:
                    self.contactManager.add_contact_to_account(account=selected_account, contact=contact)
                    self.page.close(dialog)
                
        # Gets all account options.
        def get_account_dropdown():
            options = []
            for account in self.contactManager.get_connected_accounts():
                options.append(
                    ft.DropdownOption(
                        # key turns everything into string values, so cannot use the Account object.
                        # We must turn it into a string instead that can be turned into a list.
                        key = account.service + ',' + account.address + ',' + account.applicationPassword,
                        text = account.address,
                    )
                )
            return options
        
        dropdown_account = ft.Dropdown(
            editable=False,
            label="Accounts",
            options=get_account_dropdown()
        )


        dialog = ft.AlertDialog(
            title=ft.Text("Please select an account to add this contact to"),
            content=ft.Column(
                [
                    dropdown_account
                ],
                tight=True,
            ),
            actions=[
                ft.ElevatedButton(text="Connect", on_click=close_dlg)
            ]
        )
        self.page.open(dialog)

    def fetch_contact_list(self):
        return []
    
    def get_title(self):
        return "Contacts"

    def load_contacts(self, searchTerm = None):
        noContactsText = "This account has no contacts!"
        if self.contacts == []:
            self.contacts = self.fetch_contact_list()
            self.contacts = sortContacts(self.contacts)
        if searchTerm == None or searchTerm == "":
            loadedContacts = self.contacts
        else:
            loadedContacts = searchContacts(searchTerm, self.contacts)
            noContactsText = "There are no contacts matching this search!"
        
        if len(loadedContacts) == 0:
            self.controls[-1] = ft.Row([ft.Text(noContactsText)])
        else:
            # Gets all account options.
            def make_contact_list_tiles():
                listTiles = []
                for c in loadedContacts:
                    listTiles.append(
                        ft.ListTile(
                            leading = ft.IconButton(
                                icon = ft.Icons.SEARCH,
                                icon_color = "blue200",
                                tooltip = "View Contact",
                                on_click = lambda _, contact=c: self.view_contact(contact)
                            ),  
                            title = ft.Text(c.full_name),
                            trailing = ft.TextButton(
                                text="Add to other Account",
                                on_click=lambda _, contact=c : self.add_contact_dlg(contact)
                            ),
                            on_click = lambda _, contact=c: self.view_contact(contact),
                        )
                    )
                return listTiles
                                
            self.controls[-1] = ft.ListView(
                    make_contact_list_tiles(),
                    spacing = 2,
                    divider_thickness = 2,
                    expand = True ,
                )
        self.page.update()
    
  

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
            if contact.birthday != "":
                body.append(ContactLabel("Date of Birth"))
                body.append(ContactText(contact.birthday))
            if contact.organization != "":
                body.append(ContactLabel("Organization"))
                body.append(ContactText(contact.organization[0]))
            if contact.title != "":
                body.append(ContactLabel("Title"))
                body.append(ContactText(contact.title))
            if contact.note != "":
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
                spacing = 10
            ),
        )
        self.page.open(dialog)

class AccountContactsView(ContactsView):
    def __init__(self, page: ft.Page, contactManager: ContactManager, account: Account, *args, **kwargs):
        self.account = account
        super().__init__(page, contactManager, *args, **kwargs)

    def get_title(self):
        return self.account.address
    
    def fetch_contact_list(self):
        return self.contactManager.get_account_contacts(self.account)
    
class FileContactsView(ContactsView):
    def __init__(self, page: ft.Page, contactManager: ContactManager, filePath, *args, **kwargs):
        self.filePath = filePath
        super().__init__(page, contactManager, *args, **kwargs)

    def get_title(self):
        return os.path.basename(self.filePath)
    
    def fetch_contact_list(self):
        return self.contactManager.get_file_contacts(self.filePath)
