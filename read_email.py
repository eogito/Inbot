from __future__ import print_function

import html
import os.path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify', 'https://mail.google.com/']


# Gets credentials if user is not already logged in
def get_credentials():
    creds = None

    # Check if the token file exists
    if os.path.exists('token.json'):
        # Load the saved credentials from the file
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If the credentials don't exist or are invalid, prompt the user to log in
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        # Save the credentials to the token file for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


# Reads all unread emails and marks them as read
def get_emails():
    emails = []
    creds = get_credentials()
    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(maxResults=500, userId='me', labelIds=['INBOX'],
                                              q='is:unread').execute()

    messages = results.get('messages', [])
    if messages:
        for message in messages[::-1]:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            # Mark all emails as read
            service.users().messages().modify(userId='me', id=message['id'],
                                              body={'removeLabelIds': ['UNREAD']}).execute()
            payload = msg['payload']
            headers = payload['headers']

            sender = ''
            subject = ''

            for header in headers:
                if header['name'] == 'From':
                    sender = header['value']

            for header in headers:
                if header['name'] == 'Subject':
                    subject = header['value']
            if subject == "":
                subject = "(No Subject)"

            body = msg['snippet']
            emails.append(
                ["You have a new message from: " + sender, "Subject: " + html.unescape(subject), html.unescape(body) + "..."])
    return emails
