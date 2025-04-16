import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
from helpers import Account
import getGoogleContacts as google
import getYahooContacts as yahoo
from VCFparser import VCF_parser, ContactPhone, ContactEmail, Contact

class ContactManager():
    def __init__(self, backup_dir = "./backups"):
        self.defaultBackupDir = backup_dir
        self.connectedAccounts = {}
        self.credentials_file = "./credentials"
    
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
            self.save_credentials("ReplaceThisStringWithPassword")
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
        
    def generate_key(self, password: str, salt: bytes) -> bytes:
        '''Generate encryption key from password and salt'''
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def save_credentials(self, master_password: str) -> bool:
        ''' Save credentials to a file, returns true if successful'''
        if not self.connectedAccounts:
            return False
        
        # Prepare data to encrypt
        creds_data = {}
        for account in self.connectedAccounts:
            creds_data[account.address] = {
                "service": account.service,
                "password": account.applicationPassword
            }

        # Generate salt and key
        salt = os.urandom(16)
        key = self.generate_key(master_password, salt)
        cipher_suite = Fernet(key)

        # Encrypt data
        encrypted_data = cipher_suite.encrypt(json.dumps(creds_data).encode())

        # Store salt and data
        to_store = {
            "salt": base64.urlsafe_b64encode(salt).decode(),
            "data": base64.urlsafe_b64encode(encrypted_data).decode()
        }

        try:
            with open(self.credentials_file, "w") as f:
                json.dump(to_store, f)
            return True
        except Exception as e:
            print(f"Error saving credentials: {e}")
            return False
        
    def load_credentials(self, master_password: str) -> dict[str, Account]:
        ''' Load and decrypt credentials, returns a dictionary of accounts'''
        
        if not os.path.exists(self.credentials_file):
            return {}
        try:
            with open(self.credentials_file, "r") as f:
                stored_data = json.load(f)

            salt = base64.urlsafe_b64decode(stored_data["salt"].encode())
            encrypted_data = base64.urlsafe_b64decode(stored_data["data"].encode())

            # Generate key and decrypt data
            key = self.generate_key(master_password, salt)
            cipher_suite = Fernet(key)

            decrypted_data = json.loads(cipher_suite.decrypt(encrypted_data).decode())

            # Convert to Account objects
            accounts = {}
            for email, data in decrypted_data.items():
                accounts[email] = Account(
                    address=email,
                    service=data["service"],
                    applicationPassword=data["password"]
                )
            return accounts
        except Exception as e:
            print(f"Error loading credentials: {e}")
            return {}