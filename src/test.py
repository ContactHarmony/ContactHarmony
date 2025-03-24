import pytest
import os
import getGoogleContacts as google
from helpers import Account
from contact_manager import ContactManager

# class TestGoogle():
#     def test_get_google_contacts_false(self):
#         result = google.get_google_contacts("fake_email@fake.com", "rweqhgdfsamvb432")
#         assert result == False

#     def test_get_google_contacts_true(self):
#         result = google.get_google_contacts("d6genis@gmail.com", "thyyjvntdrkfydhn")
#         assert result == True
#         os.remove("backups/contacts_combined.vcf")

#     def test_get_google_contacts_correct_backup(self):
#         google.get_google_contacts("d6genis@gmail.com", "thyyjvntdrkfydhn")
#         correct = """BEGIN:VCARD
#     VERSION:3.0
#     N:Fakename;Stacey;;;
#     FN:Stacey Fakename
#     REV:2025-03-19T19:25:20Z
#     UID:32c9e360b37a10e
#     BDAY;VALUE=DATE:1921-06-12
#     item2.TEL;TYPE=PREF:+9312345678900
#     item1.EMAIL;TYPE=PREF:fake@fake.com
#     item1.X-ABLabel:
#     item2.X-ABLabel:
#     END:VCARD\n"""
#         assert open("contacts_google/contacts_combined.vcf").read() == correct

#     def test_fetch_contacts_list_wrong_info(self):
#         hrefs_test = google.fetch_contacts_list("fake_email@fake.com", "rweqhgdfsamvb432")
#         assert hrefs_test == []

#     def test_fetch_contacts_list_correct_info(self):
#         hrefs_test = google.fetch_contacts_list("d6genis@gmail.com", "thyyjvntdrkfydhn")
#         assert hrefs_test == ['/carddav/v1/principals/d6genis@gmail.com/lists/default/',
#                             '/carddav/v1/principals/d6genis@gmail.com/lists/default/32c9e360b37a10e']

class TestContactManager():
    def test_connecting_invalid_account_should_fail(self):
        contactManager = ContactManager()
        invalidAccount = Account("google", "fake_email@fake.com", "rweqhgdfsamvb432")
        with pytest.raises(Exception):
            contactManager.connect_account(invalidAccount)
        assert invalidAccount not in contactManager.get_connected_accounts()
        assert os.path.exists(os.path.join(contactManager.defaultBackupDir, contactManager.generate_file_name(invalidAccount))) == False

    def test_connecting_valid_account_should_succeed(self):
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