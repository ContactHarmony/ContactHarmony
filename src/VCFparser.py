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
        self.current_contact = Contact()
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
        self.current_contact.first_name = vcard.contents['n'][0].value.given if 'n' in vcard.contents else ''

        self.current_contact.last_name = vcard.contents['n'][0].value.family if 'n' in vcard.contents else ''

        self.current_contact.full_name = vcard.contents['fn'][0].value if 'fn' in vcard.contents else ''

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
    
    # Given a contact object, convert back to a vcf string
    def contact_to_vcf(self, in_contact : Contact):
        vcard_text = vobject.vCard()
        vcard_text.add('n')
        vcard_text.n.value = vobject.vcard.Name( family = in_contact.last_name, given = in_contact.first_name )
        vcard_text.add('fn')
        vcard_text.fn.value = in_contact.first_name + in_contact.last_name

        vcard_text.add('tel')
        for phone in in_contact.phones:
            vcard_text.tel.value = phone.number
            vcard_text.tel.type_param = phone.type
        
        vcard_text.add('email')
        for phone in in_contact.phones:
            vcard_text.email.value = phone.number
            vcard_text.email.type_param = phone.type
        
        vcard_text.add('org')
        vcard_text.org.value = in_contact.organization
        vcard_text.add('title')
        vcard_text.title.value = in_contact.title
        vcard_text.add('note')
        vcard_text.note.value = in_contact.note
        vcard_text.add('bday')
        vcard_text.bday.value = in_contact.birthday

        vcard_text = vcard_text.serialize()

        return vcard_text
