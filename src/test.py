import pytest
import os
import shutil
import vobject
import getGoogleContacts as google
import VCFparser as vcfp
from helpers import Account
from contact_manager import ContactManager

SAMPLE_VCARD = """BEGIN:VCARD
VERSION:3.0
N:Fakename;Stacey;;;
FN:Stacey Fakename
REV:2025-03-19T19:25:20Z
UID:32c9e360b37a10e
BDAY;VALUE=DATE:1921-06-12
item2.TEL;TYPE=PREF:+9312345678900
item1.EMAIL;TYPE=PREF:fake@fake.com
item1.X-ABLabel:
item2.X-ABLabel:
END:VCARD\n"""

SAMPLE_VCARD_NO_FN = """BEGIN:VCARD
VERSION:3.0
N:Fakename;Stacey;;;
REV:2025-03-19T19:25:20Z
UID:32c9e360b37a10e
BDAY;VALUE=DATE:1921-06-12
item2.TEL;TYPE=PREF:+9312345678900
item1.EMAIL;TYPE=PREF:fake@fake.com
item1.X-ABLabel:
item2.X-ABLabel:
END:VCARD\n"""

ACCOUNT_GOOGLE_INVALID = Account('google', 'fake_email@fake.com', 'rweqhgdfsamvb432')
ACCOUNT_GOOGLE_VALID = Account('google', 'd6genis@gmail.com', 'thyyjvntdrkfydhn')

def get_temp_dir(tmp_path):
    return tmp_path / "test_output"

class TestGoogle():
    def test_get_google_contacts_false(self, tmp_path):

        result = google.get_google_contacts(ACCOUNT_GOOGLE_INVALID.address, ACCOUNT_GOOGLE_INVALID.applicationPassword, get_temp_dir(tmp_path), 'temp.vcf')
        assert result == False

    def test_get_google_contacts_true(self, tmp_path):
        result = google.get_google_contacts(ACCOUNT_GOOGLE_VALID.address, ACCOUNT_GOOGLE_VALID.applicationPassword, get_temp_dir(tmp_path), 'temp.vcf')
        assert result == True

    def test_get_google_contacts_correct_backup(self, tmp_path):
        dir = get_temp_dir(tmp_path)
        google.get_google_contacts(ACCOUNT_GOOGLE_VALID.address, ACCOUNT_GOOGLE_VALID.applicationPassword, dir, 'temp.vcf')
        correct = """BEGIN:VCARD
    VERSION:3.0
    N:Fakename;Stacey;;;
    FN:Stacey Fakename
    REV:2025-03-19T19:25:20Z
    UID:32c9e360b37a10e
    BDAY;VALUE=DATE:1921-06-12
    item2.TEL;TYPE=PREF:+9312345678900
    item1.EMAIL;TYPE=PREF:fake@fake.com
    item1.X-ABLabel:
    item2.X-ABLabel:
    END:VCARD\n"""
        assert open(os.path.join(dir, 'temp.vcf')).read() == correct

    def test_fetch_contacts_list_wrong_info_should_return(self):
        hrefs_test = google.fetch_contacts_list(ACCOUNT_GOOGLE_INVALID.address, ACCOUNT_GOOGLE_INVALID.applicationPassword)
        assert hrefs_test == []

    def test_fetch_contacts_list_correct_info(self):
        hrefs_test = google.fetch_contacts_list(ACCOUNT_GOOGLE_VALID.address, ACCOUNT_GOOGLE_VALID.applicationPassword)
        assert hrefs_test == ['/carddav/v1/principals/d6genis@gmail.com/lists/default/',
                            '/carddav/v1/principals/d6genis@gmail.com/lists/default/32c9e360b37a10e']

class TestContactManager():
    def test_connecting_invalid_account_should_fail(self, tmp_path):
        contactManager = ContactManager(backup_dir=get_temp_dir(tmp_path))
        invalidAccount = ACCOUNT_GOOGLE_INVALID
        with pytest.raises(Exception):
            contactManager.connect_account(invalidAccount)
        assert invalidAccount not in contactManager.get_connected_accounts()
        assert os.path.exists(os.path.join(contactManager.defaultBackupDir, contactManager.generate_file_name(invalidAccount))) == False

    def test_connecting_valid_google_account_should_succeed(self, tmp_path):
        contactManager = ContactManager(backup_dir=get_temp_dir(tmp_path))
        validAccount = ACCOUNT_GOOGLE_VALID
        contactManager.connect_account(validAccount)
        assert validAccount in contactManager.connectedAccounts
        backupPath = contactManager.connectedAccounts[validAccount]
        assert os.path.exists(backupPath)
    
    def test_remove_account_should_remove_backup(self, tmp_path):
        contactManager = ContactManager(backup_dir=get_temp_dir(tmp_path))
        account = ACCOUNT_GOOGLE_VALID
        contactManager.connect_account(account)
        backupPath = contactManager.connectedAccounts[account]
        contactManager.remove_account(account)
        assert account not in contactManager.connectedAccounts
        assert os.path.exists(backupPath) == False
    
    def test_get_connected_accounts_should_return_all_connected_accounts(self, tmp_path):
        contactManager = ContactManager(backup_dir=get_temp_dir(tmp_path))
        accounts = [
            ACCOUNT_GOOGLE_VALID #TODO Add a Yahoo and iCloud accoutn in here
        ]
        for a in accounts:
            contactManager.connect_account(a)
        connectedAccounts = contactManager.get_connected_accounts()
        assert connectedAccounts == accounts

    def test_all_supported_services_should_be_implemented(self, tmp_path):
        contactManager = ContactManager(backup_dir=get_temp_dir(tmp_path))
        supportedServices = contactManager.get_supported_services()
        for service in supportedServices:
            account = ACCOUNT_GOOGLE_INVALID
            with pytest.raises(Exception) as exc:
                contactManager.connect_account(account)
            assert str(exc.value) != f"{service} support not implemented!"

class TestVCFparser():
    def test_save_vcard_full_name(self):
        test_parser = vcfp.VCF_parser()
        vcf = vobject.readOne(SAMPLE_VCARD)
        first_name = vcf.contents['fn'][0].value if 'fn' in vcf.contents else ''
        test_parser.save_vcard(vcf)
        assert first_name == test_parser.contacts[0].full_name

    def test_save_vcard_full_name_with_no_fn(self):
        test_parser = vcfp.VCF_parser()
        vcf = vobject.readOne(SAMPLE_VCARD_NO_FN)
        first_name_empty = vcf.contents['fn'][0].value if 'fn' in vcf.contents else ''
        test_parser.save_vcard(vcf)
        assert first_name_empty == test_parser.contacts[0].full_name

    def test_save_vcard_email(self):
        test_parser = vcfp.VCF_parser()
        vcard = vobject.readOne(SAMPLE_VCARD)
        #first_email = vcard.contents[]