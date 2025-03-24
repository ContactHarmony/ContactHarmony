class Account():
    def __init__(self, service, address, applicationPassword):
        self.service = service  # type of account, e.g 'google' or 'yahoo'
        self.address = address
        self.applicationPassword = applicationPassword

    def __eq__(self, other):
        return (self.service == other.service and self.address == other.address and self.applicationPassword == other.applicationPassword)
    def __hash__(self):
        return hash(self.applicationPassword)