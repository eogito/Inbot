from __future__ import print_function

import os.path
from credential_check import credential_by_tag
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


def send_email(uid,to, subject=None, body='', attachment=None):
    creds = credential_by_tag(uid)
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
        return True
    except HttpError as error:
        print(F'An error occurred: {error}')
        return False