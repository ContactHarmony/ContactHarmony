from VCFparser import Contact
from rapidfuzz import fuzz

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
    MINRATIO = 75
    
    matchRatios = []
    for c in contacts:
        contactStr = c.full_name.lower()
        # addressStr =
        ratio = fuzz.partial_token_set_ratio(searchTerm, contactStr)
        if ratio >= MINRATIO:
            print(f"Contact: {c.full_name}, Ratio: {ratio}")
            matchRatios.append((c, ratio))

    matchRatios.sort(key=lambda m: m[1], reverse=True)
    matches = [m[0] for m in matchRatios]

    return matches

def sortContacts(contacts: list[Contact]):
    return sorted(contacts, key=lambda c: c.full_name)