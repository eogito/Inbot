import mysql.connector
from __future__ import print_function

import html
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify', 'https://mail.google.com/']


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="databasetest"
)
mycursor=mydb.cursor()

def credentialByTag(discordTag):
    creds = None
    #query
    query = "SELECT * FROM customers WHERE name = %s;"
    val = (discordTag,)
    mycursor.execute(query, val)
    result = mycursor.fetchall()

    if len(result)!=0:
        creds = Credentials.from_authorized_user_info(result[1], SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        # Save the credentials to the token file for future use
        tokenValue=creds.to_json()

        query = "INSERT INTO customers (name, address) VALUES (%s, %s);"
        val = (discordTag, tokenValue)
        mycursor.execute(query, val)
        mydb.commit()

    return creds