from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import os
import csv, urllib.request

def patch_drive_csv():
    #getting the url
    #hoping to make it so that it iterates thru urls
    url = ''
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)

    for row in cr:
        print(row)

def update(DRIVE, filename, mimeType):
    body = {'name': filename}
    if mimeType:
        body['mimeType'] = mimeType
    res = DRIVE.files().update(body=body, media_body=filename).execute()
    print('Uploaded "%s" (%s)' %(filename, mimeType))

def create(DRIVE, filename, mimeType):
    body = {'name': filename}
    if mimeType:
        body['mimeType'] = mimeType
    res = DRIVE.files().create(body=body, media_body=filename).execute()
    print('Uploaded "%s" (%s)' %(filename, mimeType))

# print(get_file('1QX7xKIRCmsFK6t0NqmJnXy0IVgat2NtKI_OhV6Jqc88')['name'])

SCOPES = ['https://www.googleapis.com/auth/drive.file']
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_id.json', scope=SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

FILES = (('hello.txt', None),
        ('hello.csv', 'application/vnd.google-apps.document'))

for filename, mimeType in FILES:
    create(DRIVE, filename, mimeType)