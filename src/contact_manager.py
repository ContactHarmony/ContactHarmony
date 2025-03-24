import os
from helpers import Account
import getGoogleContacts as google


class ContactManager():
    def __init__(self):
        self.backupDir = "./backups"
        self.connectedAccounts = {}
    
    def connect_account(self, account: Account):
        '''Attempt to connect an account to the ContactManager.'''

        status = False
        if account in self.connectedAccounts:
            backupPath = self.connectedAccounts[account]
        else:
            backupPath = os.path.join(self.backupDir, f"{account.service}_{account.address.partition("@")[0]}.vcf"())

        # call appropriate API to fetch contacts from service
        match account.service:
            case "google":
                status = google.get_google_contacts(account.address, account.applicationPassword, backupPath) #TODO update this function to take in a target file!
            case _:
                raise Exception(account.service + " support not implemented!")
        
        if status == True:
            self.connectedAccounts[account] = backupPath
        else:
            os.remove(backupPath)   #TODO if used on existing account, return to previous version
            raise Exception(f"Failed to fetch contacts from {account.address}")
        
    def refresh(self):
        '''refetch contacts for all connected accounts'''
        for account in self.connectedAccounts:
            self.connect_account(account)
            
    def remove_account(self, account: Account):
        '''removes a connected account'''
        if account in self.connectedAccounts:
            os.remove(self.connectedAccounts[account])
            del self.connectedAccounts[account]
        
    