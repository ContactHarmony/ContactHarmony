from VCFparser import Contact

class Account():
    def __init__(self, service, address, applicationPassword):
        self.service = service  # type of account, e.g 'google' or 'yahoo'
        self.address = address
        self.applicationPassword = applicationPassword

    def __eq__(self, other):
        return (self.service == other.service and self.address == other.address)
    def __hash__(self):
        return hash(self.applicationPassword)
    
def searchContacts(searchTerm: str, contacts: list[Contact]):
    searchTerm = searchTerm.lower()
    matches = [c for c in contacts if searchTerm in c.full_name.lower()]
    return matches