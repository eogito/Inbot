from __future__ import print_function

import os.path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# Base 64 for attachments
import base64
# Send emails
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import requests

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


def send_email(to, subject=None, body='', attachment=None):
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    # Create a new email message with attachments
    message = MIMEMultipart()
    message['to'] = to
    message['subject'] = subject
    if body:
        message.attach(MIMEText(body))

    # Checks attachment path and adds attachment if specified
    if attachment:
        url = str(attachment)
        file = requests.get(url)
        if file.status_code != 200:
            print("Failed to download attachment from URL")
        else:
            content_type = file.headers["content-type"]
            filename = "attachment." + content_type.split("/")[-1]
            attachment_data = MIMEApplication(file.content, _subtype=content_type.split("/")[-1])
            attachment_data.add_header('Content-Disposition', 'attachment', filename=filename)
            message.attach(attachment_data)

    # Convert to sendable format
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send the email with the Gmail API
    try:
        message = service.users().messages().send(
            userId='me', body={'raw': raw_message}).execute()
        print(F'Sent message to {to} Message Id: {message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')