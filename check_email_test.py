from __future__ import print_function

import html
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# Date and time
from datetime import datetime, timezone, timedelta
# Task scheduler
from apscheduler.schedulers.blocking import BlockingScheduler

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
def read_email():
    creds = get_credentials()
    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(maxResults=500, userId='me', labelIds=['INBOX'],
                                              q='is:unread').execute()

    try:
        messages = results.get('messages', [])
        if not messages:
            print("You have no new messages.")
        else:
            for message in messages[::-1]:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                # Mark all emails as read
                service.users().messages().modify(userId='me', id=message['id'],
                                                  body={'removeLabelIds': ['UNREAD']}).execute()
                email_data = msg['payload']['headers']
                for values in email_data:
                    name = values['name']
                    if name == "From":
                        from_name = values['value']
                        print("You have a new message from: " + from_name)

                        # Get email subject
                        subject = ""
                        for val in email_data:
                            if val['name'] == "Subject":
                                subject = val['value']
                        if subject == "":
                            subject = "(No Subject)"

                        print("Subject:", html.unescape(subject))
                        print(html.unescape(msg['snippet']))
                        print('\n')

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


# Define a function to check for new emails
def check_email():
    now = datetime.now(timezone.utc)
    one_minute_ago = now - timedelta(seconds=1)
    query = f'after:{one_minute_ago.strftime("%Y/%m/%d %H:%M:%S")}'

    try:
        page_token = None
        num_unread = 0
        while True:
            results = service.users().messages().list(
                userId="me", q="is:unread in:inbox", labelIds=['INBOX'], maxResults=500, pageToken=page_token
            ).execute()
            messages = len(results.get("messages", []))
            num_unread = num_unread + messages

            # Check if there are more pages to retrieve
            page_token = results.get("nextPageToken")
            if not page_token:
                break
        print(f'{num_unread} new messages received since {one_minute_ago}')
    except HttpError as error:
        print(f'An error occurred: {error}')


# Set up a scheduler to run the email check every minute
scheduler = BlockingScheduler()

# Test
creds = get_credentials()
service = build('gmail', 'v1', credentials=creds)

if creds:
    scheduler.add_job(read_email, 'interval', seconds=1)
    scheduler.start()
