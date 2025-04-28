# Contact Harmony
Software Engineering II Contact Backup Project.
Contact Harmony is a desktop application designed to save, organize, and backup contacts that uses google's [CardDav](https://datatracker.ietf.org/doc/html/rfc6352) protocol. The application currently only works for google, though we are close to developing functionality for yahoo and icloud. Contact Harmony saves your contacts completely locally, so you don't have to worry about security!

There is not yet an installation for Contact Harmony, so you must follow the Build instructions below.

## Build
To build the application, execute the following steps:
1. Set up Python 3.10
2. Install dependencies using the following terminal commands:
    - ```python -m pip install --upgrade pip```
    - ```pip install -r requirements.txt```
3. The application is now ready to be run using the following terminal command at the root folder: ```flet run```
## How To Use
Once the application is run using the steps in Build, a window appears on the desktop. The top right has two buttons:
1. **Connect Account** opens a dialog that takes an email and an application password. Once ```connect``` is pressed after the right information is entered, the account is connected and the information is saved between sessions. The account appears under ```Your Backups```. The backups also appears in the Contact Harmony directory under the ```./backup``` subdirectory.
   1. To get your application password for a **google** account, follow google's guide [here](https://support.google.com/accounts/answer/185833?hl=en) or follow the link [here](https://myaccount.google.com/apppasswords).
   2. To get your application password for a **yahoo** account, follow yahoo's guide [here](https://help.yahoo.com/kb/SLN15241.html).
2. **Open vcf** lets the user open any vcf file on their desktop at will and browse or search through the contacts. This works offline.
There are also two buttons on the top left.
1. **Refresh Contact Backups** appears as a circle-arrow. When clicked, it refreshes all the connected accounts to keep them up to date.
2. **Browse All Contacts** is a person-search icon that lets the user browse all contacts from all connected accounts.
Lastly, the main part of the window features tiles for all connected accounts. The accounts can be disconnected with the red trash button, or the contacts can be browsed through via the ```browse contacts``` button. This opens a list of all contacts under that account that can be browsed and searched through. When clicked, each contact opens more information on the contact. Each contact can also be added to another connected account.

### Unit Tests
To run the unit tests for this application, first install the dependencies using the terminal commands in step 2 above.
Then, type the following terminal command at the root folder: ```pytest src/test.py```
