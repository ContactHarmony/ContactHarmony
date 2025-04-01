import pytest
import os
import getGoogleContacts as google
from helpers import Account
from contact_manager import ContactManager


class TestContactManager():
    def test_connecting_invalid_account_should_fail(self):
        contactManager = ContactManager()
        invalidAccount = Account("google", "fake_email@fake.com", "rweqhgdfsamvb432")
        with pytest.raises(Exception):
            contactManager.connect_account(invalidAccount)
        assert invalidAccount not in contactManager.get_connected_accounts()
        assert os.path.exists(os.path.join(contactManager.defaultBackupDir, contactManager.generate_file_name(invalidAccount))) == False

    def test_connecting_valid_google_account_should_succeed(self):
        contactManager = ContactManager()
        validAccount = Account("google", "d6genis@gmail.com", "thyyjvntdrkfydhn")
        contactManager.connect_account(validAccount)
        assert validAccount in contactManager.connectedAccounts
        backupPath = contactManager.connectedAccounts[validAccount]
        assert os.path.exists(backupPath)
    
    def test_remove_account_should_remove_backup(self):
        contactManager = ContactManager()
        account = Account("google", "d6genis@gmail.com", "thyyjvntdrkfydhn")
        contactManager.connect_account(account)
        backupPath = contactManager.connectedAccounts[account]
        contactManager.remove_account(account)
        assert account not in contactManager.connectedAccounts
        assert os.path.exists(backupPath) == False
    
    def test_get_connected_accounts_should_return_all_connected_accounts(self):
        contactManager = ContactManager()
        accounts = [
            Account("google", "d6genis@gmail.com", "thyyjvntdrkfydhn"),
            Account("google", "infoserach@gmail.com", "kugoyrkqyxnplcno")
        ]
        for a in accounts:
            contactManager.connect_account(a)
        connectedAccounts = contactManager.get_connected_accounts()
        assert connectedAccounts == accounts

    def test_all_supported_services_should_be_implemented(self):
        contactManager = ContactManager()
        supportedServices = contactManager.get_supported_services()
        for service in supportedServices:
            account = Account(service, "fake_email@fake.com", "rweqhgdfsamvb432")
            with pytest.raises(Exception) as exc:
                contactManager.connect_account(account)
            assert str(exc.value) != f"{service} support not implemented!"

    
            
