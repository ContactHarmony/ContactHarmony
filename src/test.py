import pytest
from getGoogleContacts import get_google_contacts

def test_get_google_contacts_false():
    result = get_google_contacts("fake_email12345@fake.com", "rweqhgdfsamvb432")
    assert result == False

