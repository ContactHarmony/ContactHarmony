import vobject
from dataclasses import dataclass, field
from typing import List

@dataclass
class ContactPhone:
    number: str
    type: str

@dataclass
class ContactEmail:
    email: str
    type: str

@dataclass
class Contact:
    first_name: str = ''
    last_name: str = ''
    full_name: str = ''
    phones: List[ContactPhone] = field(default_factory=list)
    emails: List[ContactEmail] = field(default_factory=list)
    organization: str = ''
    title: str = ''
    note: str = ''
    birthday: str = ''

class VCF_parser:
    def __init__(self):
        self.contacts = [] #Initializing the list of contacts
        self.current_contact = None
        self.current_vcard = []

	# Parse contacts from a VCF file
    def parse_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            return self.parse(f.read())

	# Parse contact on a per line basis
    def parse(self, vcf_content):
        for line in vcf_content.split("\n"):
            self.parse_line(line)
        return self.contacts

	# Parse single line
    def parse_line(self, line):
        if line.startswith("BEGIN:VCARD"):
            self.current_contact = Contact()
            self.current_vcard = []
        self.current_vcard.append(line)
        if line.startswith("END:VCARD"):
            vcard = vobject.readOne("\n".join(self.current_vcard))
            self.save_vcard(vcard)

	# Extracting the contact information from the vCard
    def save_vcard(self, vcard):
        self.current_contact.full_name = vcard.contents.get('fn', [None])[0].value if 'fn' in vcard.contents else ''

        # Extract phone numbers
        for tel in vcard.contents.get('tel', []):
            currentPhone = ContactPhone(tel.value, tel.params.get('TYPE', ['unknown'])[0])
            self.current_contact.phones.append(currentPhone)

        # Extract emails
        for email in vcard.contents.get('email', []):
            currentEmail = ContactEmail(email.value, email.params.get('TYPE', ['unknown'])[0])
            self.current_contact.emails.append(currentEmail)

        # Extract optional fields
        self.current_contact.organization = vcard.contents.get('org', [None])[0].value if 'org' in vcard.contents else ''
        self.current_contact.title = vcard.contents.get('title', [None])[0].value if 'title' in vcard.contents else ''
        self.current_contact.note = vcard.contents.get('note', [None])[0].value if 'note' in vcard.contents else ''
        self.current_contact.birthday = vcard.contents.get('bday', [None])[0].value if 'bday' in vcard.contents else ''

        # Add the contact to the list
        self.contacts.append(self.current_contact)
