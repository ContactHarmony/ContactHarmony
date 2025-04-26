import os
import requests
import uuid
from xml.etree import ElementTree as ET

# Replace xxxxxxxxx@yahoo.com by your actual Yahoo email address
# You can use also other Yahoo domains like
# yahoo.ca, yahoo.jp, yahoo.in, yahoo.co.uk, yahoo.co.il, myyahoo.com, currently.com, att.net
#######USERNAME = "xxxxxxxxx@yahoo.com" # or xxxxxx@yahoo.co.uk or xxxxxx@currently.com etc.

#This is "Application Password", not a main Yahoo Account password
#######PASSWORD = "application_password_16_digits"  # Replace with your application-specific password

# CardDAV server details. It is not a base URL, but Address Book URL
#######CARD_DAV_URL = f"https://carddav.address.yahoo.com/dav/{USERNAME}/Contacts/"

BASE_URL = "https://carddav.address.yahoo.com/dav"

# Directory to save the contacts
OUTPUT_DIR = "./contacts_yahoo"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "yahoo_contacts.vcf")

# XML body for the PROPFIND request
PROPFIND_BODY = """<?xml version="1.0" encoding="UTF-8"?>
<d:propfind xmlns:d="DAV:">
  <d:prop>
    <d:getetag/>
    <d:resourcetype/>
    <d:displayname/>
  </d:prop>
</d:propfind>
"""



def clean_vcard(vcard_data):
    """
    Remove empty lines from the vCard data.
    """
    lines = vcard_data.splitlines()
    cleaned_lines = [line for line in lines if line.strip()]  # Remove empty or whitespace-only lines
    return "\n".join(cleaned_lines)

def fetch_contacts(email, application_password):
    """
    Fetch the list of contacts from the CardDAV server.
    """
    headers = {
        "Depth": "1",
        "Content-Type": "application/xml",
    }

    CARD_DAV_URL = f"{BASE_URL}/{email}/Contacts/"

    print("Fetching contact list from CardDAV server...")
    response = requests.request(
        "PROPFIND",
        CARD_DAV_URL,
        auth=(email, application_password),
        headers=headers,
        data=PROPFIND_BODY,
    )

    if response.status_code not in [200, 207]:
        print(f"Failed to fetch contacts list: {response.status_code}")
        print(response.content.decode("utf-8"))
        return []

    # Parse the response XML
    root = ET.fromstring(response.content)
    ns = {"d": "DAV:"}
    hrefs = []

    # Extract hrefs for .vcf files
    for response in root.findall("d:response", ns):
        href = response.find("d:href", ns)
        if href is not None and href.text.endswith(".vcf"):
            hrefs.append(href.text)

    return hrefs

def fetch_contact_data(hrefs, combined_file, email, application_password):
    """
    Fetch the data for a single contact and return it as text.
    """
    if hrefs.startswith("/"):
        contact_full_url = "https://carddav.address.yahoo.com" + hrefs
    elif hrefs.startswith("http"):
        contact_full_url = hrefs
    else:
        contact_full_url = combined_file.rstrip("/") + "/" + hrefs.lstrip("/")

    print(f"Fetching contact: {contact_full_url}")
    response = requests.get(contact_full_url, auth=(email, application_password))

    if response.status_code == 200:
        return clean_vcard(response.text)  # Clean the vCard data
    else:
        print(f"Failed to fetch contact {hrefs}: {response.status_code}")
        print(response.content.decode("utf-8"))
        return None

def save_contacts_to_file(hrefs, combined_file, email, application_password):
    """
    Save all contact data into a single VCF file.
    """
    with open(combined_file, "w", encoding="utf-8") as f:
        for href in hrefs:
            contact_data = fetch_contact_data(href, combined_file, email, application_password)
            if contact_data:
                f.write(contact_data)
                f.write("\n")  # Ensure each contact is separated by a newline

    print(f"Contacts saved to {combined_file}")

def get_yahoo_contacts(email, application_password, directory, fname):
    # make sure directory exists and create file
    if not os.path.exists(directory):
        os.makedirs(directory)
    combined_file_path = os.path.join(directory, fname)

    # fetch the list of contacts
    hrefs = fetch_contacts(email, application_password)
    print(f"Found {len(hrefs)} contacts.")
    if hrefs == []:
        return False

    # save all contacts into a single file
    save_contacts_to_file(hrefs, combined_file_path, email, application_password)
    return True

# Add a new contact to a Yahoo CardDAV address book using POST (RFC 5995).
def post_contact_to_yahoo_account(vcard, email, application_password):
    uid = str(uuid.uuid4())
    contact_url = f"{BASE_URL}/{email}/Contacts/{uid}.vcf"

    headers = {
        "Content-Type": "text/vcard; charset=utf-8"
    }

    response = requests.put(
        contact_url,
        auth=(email, application_password),
        headers=headers,
        data=vcard.encode("utf-8")
    )

    if response.status_code in [200, 201, 204]:
        print(f"Contact created at {contact_url}")
        return contact_url
    else:
        print(f"Failed to create contact: {response.status_code}")
        print(response.content.decode("utf-8"))
        return None


"""if __name__ == "__main__":
    # Fetch the list of contacts
    contacts = fetch_contacts()
    print(f"Found {len(contacts)} contacts.")

    # Save all contacts into a single file
    save_contacts_to_file(contacts, OUTPUT_FILE)"""