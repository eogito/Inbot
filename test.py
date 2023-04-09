from __future__ import print_function

import html
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
# Base 64 for attachments
import base64
# Send emails
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import requests

SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify', 'https://mail.google.com/']

flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('gmail', 'v1', credentials=creds)

# Create a new email message with attachments
message = MIMEMultipart()
message['to'] = 'felix.zhao2@student.tdsb.on.ca'
message['subject'] = 'hi'
message.attach(MIMEText('hi glen'))

# Convert to sendable format
raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

# Send the email with the Gmail API
try:
    message = service.users().messages().send(
        userId='me', body={'raw': raw_message}).execute()
    print(F'Sent message to Message Id: {message["id"]}')
except HttpError as error:
    print(F'An error occurred: {error}')