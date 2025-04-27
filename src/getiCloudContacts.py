import os
import requests
from xml.etree import ElementTree as ET

# CardDAV server details
BASE_URL = "https://contacts.icloud.com"

def clean_vcard(content):
    lines = content.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned_lines)

def save_contact(filename, content, combined_file):
    cleaned_content = clean_vcard(content)
    with open(combined_file, "a", encoding="utf-8") as combined_vcf:
        combined_vcf.write(cleaned_content + "\n")
    print(f"Added contact {filename} to combined file: {combined_file}")

def fix_contacts_if_long(preprocessed_lines):
    combined_lines = ""
    previous_line = ""
    for line in preprocessed_lines.split("\r\n"):
        line = line.strip()
        if ":" not in line and len(previous_line) == 75:
            previous_line += line
            combined_lines += previous_line
            previous_line = ""
        else:
            combined_lines += previous_line + "\n"
            previous_line = line
    return combined_lines

def discover_icloud_carddav_urls(username, password):
    """
    Discover the user's principal and address book URLs on iCloud.
    """
    headers = {
        "Depth": "0",
        "Content-Type": "application/xml",
    }
    body = """<?xml version="1.0" encoding="UTF-8"?>
    <d:propfind xmlns:d="DAV:" xmlns:cs="http://calendarserver.org/ns/">
      <d:prop>
        <d:current-user-principal/>
      </d:prop>
    </d:propfind>"""

    response = requests.request(
        "PROPFIND", BASE_URL + "/", auth=(username, password), headers=headers, data=body
    )

    if response.status_code not in [200, 207]:
        print(f"Failed to discover principal: {response.status_code}")
        print(response.content.decode("utf-8"))
        return None

    root = ET.fromstring(response.content)
    ns = {"d": "DAV:"}

    principal_href = root.find(".//d:href", ns)
    if principal_href is None:
        print("Principal href not found.")
        return None

    principal_url = BASE_URL + principal_href.text

    # Now find the address book home set
    body2 = """<?xml version="1.0" encoding="UTF-8"?>
    <d:propfind xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
      <d:prop>
        <card:addressbook-home-set/>
      </d:prop>
    </d:propfind>"""

    response2 = requests.request(
        "PROPFIND", principal_url, auth=(username, password), headers=headers, data=body2
    )

    if response2.status_code not in [200, 207]:
        print(f"Failed to discover addressbook-home-set: {response2.status_code}")
        print(response2.content.decode("utf-8"))
        return None

    root2 = ET.fromstring(response2.content)
    card_ns = {"card": "urn:ietf:params:xml:ns:carddav", "d": "DAV:"}

    addressbook_home_href = root2.find(".//d:href", card_ns)
    if addressbook_home_href is None:
        print("Addressbook-home-set href not found.")
        return None

    addressbook_url = BASE_URL + addressbook_home_href.text

    return addressbook_url

def fetch_contacts_list(username, password):
    """
    Fetch the list of contact URLs from the address book.
    """
    addressbook_url = discover_icloud_carddav_urls(username, password)
    if not addressbook_url:
        return []

    headers = {
        "Depth": "1",
        "Content-Type": "application/xml",
    }
    body = """<?xml version="1.0" encoding="UTF-8"?>
    <d:propfind xmlns:d="DAV:" xmlns:card="urn:ietf:params:xml:ns:carddav">
      <d:prop>
        <d:getetag/>
        <d:displayname/>
        <d:resourcetype/>
      </d:prop>
    </d:propfind>"""

    response = requests.request(
        "PROPFIND", addressbook_url, auth=(username, password), headers=headers, data=body
    )

    if response.status_code not in [200, 207]:
        print(f"Failed to fetch contacts list: {response.status_code}")
        print(response.content.decode("utf-8"))
        return []

    root = ET.fromstring(response.content)
    ns = {"d": "DAV:"}
    hrefs = []

    for response in root.findall("d:response", ns):
        href = response.find("d:href", ns)
        if href is not None:
            hrefs.append(href.text)
    return hrefs

def fetch_contact(href, combined_file, username, password):
    """
    Fetch a single contact and add it to the combined file.
    """
    url = BASE_URL + href
    response = requests.get(url, auth=(username, password))

    if response.status_code == 200:
        un_fixed_content = response.content.decode("utf-8")
        vcard_content = fix_contacts_if_long(un_fixed_content)
        filename = href.split("/")[-1]
        save_contact(filename, vcard_content, combined_file)
        return True
    else:
        print(f"Failed to fetch contact {href}: {response.status_code}")
        print(response.content.decode("utf-8"))
        return False

def get_icloud_contacts(username, password, directory, fname):
    """
    Main function to fetch all contacts and save them.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    combined_file_path = os.path.join(directory, fname)

    hrefs = fetch_contacts_list(username, password)
    if hrefs == []:
        return False

    with open(combined_file_path, "w", encoding="utf-8") as combined_vcf:
        combined_vcf.write("")  # Start with empty file

    print(f"Found {len(hrefs)-1} contacts.")
    print(hrefs)
    for href in hrefs[1:]:
        fetch_contact(href, combined_file_path, username, password)
    return True