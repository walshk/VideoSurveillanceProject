"""

THIS CODE FROM STACKOVERFLOW USER roshan
https://stackoverflow.com/questions/37960035/python-email-errno-10061-no-connection-could-be-made-because-the-target-machi?rq=1

"""


from __future__ import print_function
import httplib2
import os

from email.mime.text import MIMEText
import base64
from googleapiclient.errors import HttpError


from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
   import argparse
   flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
   flags = None

# If modifying these scopes, delete your previously saved credentials 
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = "https://mail.google.com/"
CLIENT_SECRET_FILE = '../client_secret.json' # replace with your own Gmail API authenticator
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,
	'gmail-python-quickstart.json')

	store = oauth2client.file.Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

# create a message
def CreateMessage(sender, to, subject, message_text):
	message = MIMEText(message_text)
	message['to'] = to
	message['from'] = sender
	message['subject'] = subject
	return {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}

#send message 
def SendMessage(service, user_id, message):
	try:
		message = (service.users().messages().send(userId=user_id, body=message).execute())
		#print 'Message Id: %s' % message['id']
		return message
	except(HttpError):
		print ('An error occurred')


def SendAlert(recipient, subject, body):
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)


	message = CreateMessage(recipient, recipient, subject, body)
	SendMessage(service, "me", message)
	print("Alert Log sent to user")