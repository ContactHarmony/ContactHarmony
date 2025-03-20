import pytest
import os
import getGoogleContacts as google


def test_get_google_contacts_false():
    result = google.get_google_contacts("fake_email@fake.com", "rweqhgdfsamvb432")
    assert result == False

def test_get_google_contacts_true():
    result = google.get_google_contacts("d6genis@gmail.com", "thyyjvntdrkfydhn")
    assert result == True
    os.remove("contacts_google/contacts_combined.vcf")

def test_get_google_contacts_correct_backup():
    google.get_google_contacts("d6genis@gmail.com", "thyyjvntdrkfydhn")
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
    assert open("contacts_google/contacts_combined.vcf").read() == correct

def test_fetch_contacts_list_wrong_info():
    hrefs_test = google.fetch_contacts_list("fake_email@fake.com", "rweqhgdfsamvb432")
    assert hrefs_test == []

def test_fetch_contacts_list_correct_info():
    hrefs_test = google.fetch_contacts_list("d6genis@gmail.com", "thyyjvntdrkfydhn")
    assert hrefs_test == ['/carddav/v1/principals/d6genis@gmail.com/lists/default/',
                          '/carddav/v1/principals/d6genis@gmail.com/lists/default/32c9e360b37a10e']
