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

# Assume that token is a JSON string stored in your database
token = ''

# Convert the JSON string to a dictionary
info = json.loads(token)

# Create a Credentials object from the dictionary
creds = Credentials.from_authorized_user_info(info)
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
    print(F'Sent message to {to} Message Id: {message["id"]}')
except HttpError as error:
    print(F'An error occurred: {error}')