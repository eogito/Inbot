from __future__ import print_function
import mysql.connector
import html
import os.path
import json
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

def credential_by_tag(discordTag):
    discordTag=str(discordTag)
    creds = None
    #query
    query = "SELECT * FROM customers WHERE name = %s;"
    val = (discordTag,)
    mycursor.execute(query, val)
    result = mycursor.fetchall()

    if len(result)!=0 and result!=None:
        info=json.load(result[1])
        creds = Credentials.from_authorized_user_info(info=info, scopes=SCOPES)

    if not creds or not creds.valid:
        if creds!=None:
            query = "DELETE FROM customers WHERE name=%s;"
            val = (discordTag, )
            mycursor.execute(query, val)
            mydb.commit()

        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)


        tokenJson=creds.to_json()
        # Save the credentials to the token file for future use
        query = "INSERT INTO customers (name, address) VALUES (%s, %s);"
        val = (discordTag, tokenJson)
        mycursor.execute(query, val)
        mydb.commit()

    return creds
