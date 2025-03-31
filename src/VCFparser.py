import re
import vobject
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Optional

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
		first_name: str
		last_name: str
		phones: List[ContactPhone] = field(default_factory=list)
		emails: List[ContactEmail] = field(default_factory=list)
		organization: str = ''
		title: str = ''
		note: str = ''
		birthday: str = ''

		class VCF_parser:
				def init(self):
						self.contacts = []
						self.current_contact = None
						self.current_vcard = []
						self.property_name = None
						self.property_params = None
						self.property_value = None

				def parse_file(self, filename):
						# Parse contacts from a VCF file
						with open(filename, "r", encoding="utf-8") as f:
								return self.parse(f.read())

				def parse(self, vcf_content):
						# Parse contact on a per line basis
						for line in vcf_content.split("\n"):
								self.parse_line(line)
						return self.contacts

				def parse_line(self, line):
						# Parse single line
						if line.startswith("BEGIN:VCARD"):
								self.current_contact = Contact()
								self.current_vcard = []
								self.current_vcard.append(line)
						elif line.startswith("END:VCARD"):
								self.current_vcard.append(line)
								vcard=vobject.readOne(self.current_vcard)
								self.save_vcard(vcard)
						else:
								self.current_vcard.append(line)

def save_vcard(self, vcard):
					# After a vcard is parsed through, the contents are added to the class
					first_name = vcard.contents('fn')
					for tel in vcard.contents['tel']:
						currentPhone = ContactPhone(tel.value, tel.type)
						self.phones.append(currentPhone)
					for email in vcard.contents['email']:
						currentEmail = ContactEmail(email.value, email.type)
						self.emails.append(currentEmail)
					organization = vcard.contents('org')
					title = vcard.contents('title')
					note = vcard.contents('note')
					birthday = vcard.contents('bday')
