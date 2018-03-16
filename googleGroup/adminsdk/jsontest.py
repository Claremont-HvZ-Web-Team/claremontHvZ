from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import requests

SCOPES = "https://www.googleapis.com/auth/admin.directory.group"
CLIENT_SECRET = 'client_secret.json'

store = file.Storage('storage.json')
credz = store.get()
if not credz or credz.invalid:
	flow = client.flow_from_clientsecrets(CLIENT_SECRET)
	credz = tools.run(flow, store)
	SERVICE = build()
	r = requests.get('https://www.googleapis.com/admin/directory/v1/groups/hvztesinggroup@googlegroups.com/members',
	{
	   "email": "johnshi0718@gmail.com",
	    "role": "MANAGER"
	})

	data = r.json()
	return data