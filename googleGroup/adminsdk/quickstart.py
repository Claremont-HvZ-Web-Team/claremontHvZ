from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
import json
from httplib2 import Http

scopes = ['https://www.googleapis.com/auth/admin.directory.group.member',
          'https://www.googleapis.com/auth/admin.directory.group.member.readonly',
          'https://www.googleapis.com/auth/admin.directory.group',
          'https://www.googleapis.com/auth/admin.directory.group.readonly']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'HvZtesting-7947bcf08858.json',
    scopes=scopes
    )

# Use this sub email as the subject to delegate on behalf of that user
account_sub = 'charleentan1113@gmail.com'

delegate_credentials = credentials.create_delegated(account_sub)

http = credentials.authorize(Http())

directory = build('admin', 'directory_v1', http=http)

response = directory.resources().calendars().list(customer='my_customer')
print(response.execute(http=http))