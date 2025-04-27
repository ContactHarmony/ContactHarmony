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
    MINRATIO = 85
    
    matchRatios = []
    for c in contacts:
        contactNames = c.full_name.lower().split()

        ratio = 0
        priority = 0
        for index, contactStr in enumerate(contactNames):
            currentRatio = fuzz.partial_ratio(searchTerm, contactStr)
            if currentRatio > ratio:
                ratio = currentRatio
                priority = len(contactNames) - index

        if ratio >= MINRATIO:
            print(f"Contact: {c.full_name}, Ratio: {ratio}")
            matchRatios.append((c, ratio, priority))

    matchRatios.sort(key=lambda m: (m[1], m[2]), reverse=True)
    matches = [m[0] for m in matchRatios]

    return matches

def searchAccountContacts(searchTerm: str, contacts: list[tuple[Contact, Account]]):
    searchTerm = searchTerm.lower()
    MINRATIO = 85
    
    matchRatios = []
    for c in contacts:
        contactNames = c[0].full_name.lower().split()

        ratio = 0
        priority = 0
        for index, contactStr in enumerate(contactNames):
            currentRatio = fuzz.partial_ratio(searchTerm, contactStr)
            if currentRatio > ratio:
                ratio = currentRatio
                priority = len(contactNames) - index
            
        
        if ratio >= MINRATIO:
            print(f"Contact: {c[0].full_name}, Ratio: {ratio}")
            matchRatios.append((c, ratio, priority))

    matchRatios.sort(key=lambda m: (m[1], m[2]), reverse=True)
    matches = [m[0] for m in matchRatios]

    return matches

def sortContacts(contacts: list[Contact]):
    return sorted(contacts, key=lambda c: c.full_name)

def sortAccountContacts(contacts: list[tuple[Contact, Account]]):
    return sorted(contacts, key=lambda c: c[0].full_name)