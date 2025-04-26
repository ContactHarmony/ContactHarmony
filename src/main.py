import flet as ft
from app_views import HomeView, ContactsView
from contact_manager import ContactManager
from helpers import Account


if __name__ == "__main__":
 
    def contact_harmony_app(page: ft.Page):
        
        page.title = "Contact Harmony"
        page.update()
        contactManager = ContactManager()

        testGoogleAccount = Account("google", "contactharmony.test@gmail.com", "iham kmcq kjjb flxk")
        testYahooAccount = Account("yahoo", "contactharmony@yahoo.com", "fxhakkkkcriljlhj")
        # contactManager.connect_account(testGoogleAccount)
        # contactManager.connect_account(testYahooAccount)
        contactManager.load_credentials()

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

    
    ft.app(contact_harmony_app)