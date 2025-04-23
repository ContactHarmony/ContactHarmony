import os
from helpers import Account
import getGoogleContacts as google
import getYahooContacts as yahoo
from VCFparser import VCF_parser, ContactPhone, ContactEmail, Contact

class ContactManager():
    def __init__(self, backup_dir = "./backups"):
        self.defaultBackupDir = backup_dir
        self.connectedAccounts = {}
    
    def connect_account(self, account: Account):
        '''attempt to connect an account to the ContactManager.'''

        status = False
        if account in self.connectedAccounts:
            backupDirectory = os.path.dirname(self.connectedAccounts[account])
            backupFileName = os.path.basename(self.connectedAccounts[account])
        else:
            backupDirectory = self.defaultBackupDir
            backupFileName = self.generate_file_name(account)

        # call appropriate API to fetch contacts from service
        match account.service:
            case "google":
                status = google.get_google_contacts(account.address, account.applicationPassword, backupDirectory, backupFileName)
            case "yahoo":
                status = yahoo.get_yahoo_contacts(account.address, account.applicationPassword, backupDirectory, backupFileName)
            case _:
                raise Exception(f"{account.service} support not implemented!")
        
        newPath = os.path.join(backupDirectory, backupFileName)

        if status == True:
            self.connectedAccounts[account] = newPath
        else:
            if os.path.exists(newPath):
                os.remove(newPath)   #TODO if used on existing account, return to previous version
        return status
        
    def get_supported_services(self):
        '''return a list of supported services'''
        return ['google', 'yahoo'] #TODO change to return ['google', 'yahoo', 'icloud']

    def get_connected_accounts(self):
        '''returns a list of connected accounts'''
        return list(self.connectedAccounts.keys())

    def get_account_contacts(self, account: Account):
        '''returns a list of account contacts'''
        parser = VCF_parser()
        parsedContacts = parser.parse_file(self.connectedAccounts[account])
        return parsedContacts
    
    def generate_file_name(self, account: Account):
        '''return the default path for a given account'''
        return f"{account.service}_{account.address.partition('@')[0]}.vcf"
    
    def refresh(self):
        '''refetch contacts for all connected accounts'''
        for account in self.connectedAccounts:
            self.connect_account(account)
            
    def remove_account(self, account: Account):
        '''removes a connected account'''
        if account in self.connectedAccounts:
            os.remove(self.connectedAccounts[account])
            del self.connectedAccounts[account]
        
    def add_contact_to_account(self, account: Account, contact: Contact):
        parser = VCF_parser()
        vcf_string = parser.contact_to_vcf(contact)
        match account.service:
            case "google":
                google.post_contact_to_google_account(vcf_string, account.address, account.applicationPassword)
                self.connect_account(account)
            case "yahoo":
                yahoo.post_contact_to_yahoo_account(vcf_string, account.address, account.applicationPassword)
                self.connect_account(account)
            case _:
                raise Exception(f"{account.service} support not implemented!") #Should be impossible to reach at the moment