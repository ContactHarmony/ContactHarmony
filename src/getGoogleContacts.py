import os
import requests
from xml.etree import ElementTree as ET

# CardDAV server details
# Base URL for CardDAV server
BASE_URL = "https://www.google.com/carddav/v1/principals"
# Add gmail to @gmail.com by your actual Gmail email address
    #USERNAME = "infoserach@gmail.com"
#Enable 2FA and generate Application Password. You can't use your main Google password
    #PASSWORD = "kugo yrkq yxnp lcno"
# Construct the CardDAV URL
#CARD_DAV_URL = f"{BASE_URL}/{USERNAME}/lists/default/"

def clean_vcard(content):
    """
    Normalize line endings in vCard content.
    - Replace '\r\n' or '\r' with '\n'.
    - Remove any extra blank lines.
    """
    lines = content.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    cleaned_lines = [line.strip() for line in lines if line.strip()]  # Remove blank lines
    return "\n".join(cleaned_lines)

def save_contact(filename, content, combined_file):
    """
    Save the cleaned vCard data to a combined .vcf file and optionally save individual files.
    """
    cleaned_content = clean_vcard(content)  # Clean the content before saving

    # Add contact to the combined file
    with open(combined_file, "a", encoding="utf-8") as combined_vcf:
        combined_vcf.write(cleaned_content + "\n")  # Add a newline between contacts
    print(f"Added contact {filename} to combined file: {combined_file}")

    # Optionally save as individual file (commented out but kept for reference)
    # filepath = os.path.join(OUTPUT_DIR, filename + ".vcf")
    # with open(filepath, "w", encoding="utf-8") as vcf_file:
    #     vcf_file.write(cleaned_content)
    # print(f"Saved contact to {filepath}")

def fetch_contacts_list(gmail, applicationPassword):
    """
    Fetch the list of contact URLs from the address book.
    """
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

    CARD_DAV_URL = f"{BASE_URL}/{gmail}/lists/default/"

    response = requests.request(
        "PROPFIND", CARD_DAV_URL, auth=(gmail, applicationPassword), headers=headers, data=body
    )

    if response.status_code not in [200, 207]:
        print(f"Failed to fetch contacts list: {response.status_code}")
        print(response.content.decode("utf-8"))
        return []

    # Parse the response XML to extract hrefs
    root = ET.fromstring(response.content)
    ns = {"d": "DAV:"}
    hrefs = []

    for response in root.findall("d:response", ns):
        href = response.find("d:href", ns)
        if href is not None:
            hrefs.append(href.text)
    return hrefs

def fetch_contact(href, combined_file, gmail, applicationPassword):
    """
    Fetch a single contact and add it to the combined file.
    False for failure, True for success
    """
    url = "https://www.google.com" + href
    response = requests.get(url, auth=(gmail, applicationPassword))

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

# Goes through contacts to make sure there are no disconnected lines
def fix_contacts_if_long(prepreocessed_lines):
    combined_lines = ""
    previous_line = ""#prepreocessed_lines.partition("\r\n")[0]
    for line in prepreocessed_lines.split("\r\n"):
        line = line.strip()
        if ":" not in line and len(previous_line) == 75:
            previous_line = previous_line + line
            combined_lines = combined_lines + previous_line
            previous_line = ""
        else:
            combined_lines = combined_lines + previous_line + "\n"
            previous_line = line
        
    return combined_lines

def get_google_contacts(gmail, applicationPassword, directory, fname):
    # make sure output directory exists and create file
    if not os.path.exists(directory):
        os.makedirs(directory)
    combined_file_path = os.path.join(directory, fname)

    hrefs = fetch_contacts_list(gmail, applicationPassword)
    if hrefs == []:
        return False

    # Create or clear the combined file
    with open(combined_file_path, "w", encoding="utf-8") as combined_vcf:
        combined_vcf.write("")  # Start with an empty file

    # Get contacts 1-by-1
    print(f"Found {len(hrefs)-1} contacts.")
    print(hrefs)
    for href in hrefs[1:]:
        fetch_contact(href, combined_file_path, gmail, applicationPassword)
    return True

'''
if __name__ == "__main__":
    combined_file_path = os.path.join(OUTPUT_DIR, "contacts_combined.vcf")

    # Create or clear the combined file
    with open(combined_file_path, "w", encoding="utf-8") as combined_vcf:
        combined_vcf.write("")  # Start with an empty file

    hrefs = fetch_contacts_list()
    print(f"Found {len(hrefs)} contacts.")
    for href in hrefs:
        fetch_contact(href, combined_file_path)
'''