# Contact Harmony
Software Engineering II Contact Backup Project.
Contact Harmony is a desktop application designed to save, organize, and backup contacts that uses google's [CardDav](https://datatracker.ietf.org/doc/html/rfc6352) protocol. The application currently only works for google, though we are close to developing functionality for yahoo and icloud. Contact Harmony saves your contacts completely locally, so you don't have to worry about security!

There is not yet an installation for Contact Harmony, so you must follow the Build instructions below. It does not yet save your contacts.

## Build
To build the application, execute the following steps:
1. Set up Python 3.10
2. Install dependencies using the following terminal commands:
    - ```python -m pip install --upgrade pip```
    - ```pip install -r requirements.txt```
3. The application is now ready to be run using the following terminal command at the root folder: ```flet run```
### Unit Tests
To run the unit tests for this application, type the following terminal command at the root folder:
```pytest src/test.py```
