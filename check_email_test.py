from __future__ import print_function

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
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

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

# Define a function to check for new emails
def check_email():
    now = datetime.now(timezone.utc)
    one_minute_ago = now - timedelta(seconds=1)
    query = f'after:{one_minute_ago.strftime("%Y/%m/%d %H:%M:%S")}'

    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    try:
        # Call the Gmail API to retrieve the number of unread messages
        response = service.users().messages().list(
            userId='me',
            q='is:unread'
        ).execute()

        # Get the number of unread messages from the response
        num_unread = len(response['messages'])
        print(f'{len(num_unread)} new messages received since {one_minute_ago}')
    except HttpError as error:
        print(f'An error occurred: {error}')

# Set up a scheduler to run the email check every minute
scheduler = BlockingScheduler()

# Test
creds = get_credentials()

if creds:
    scheduler.add_job(check_email, 'interval', seconds=1)
    scheduler.start()
