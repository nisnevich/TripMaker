from __future__ import print_function

import base64
import os
import sys
from email.mime.text import MIMEText

import httplib2
from apiclient import discovery
from googleapiclient import errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from src.const.constants import CONFIG_ROOT
from src.util.log import Logger


class GmailAPIUtil:
    try:
        import argparse
    
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/gmail-python-quickstart.json
    SCOPES = 'https://mail.google.com/'
    CLIENT_SECRET_FILE = os.path.join(CONFIG_ROOT, 'client_secret.json')
    APPLICATION_NAME = 'Gmail API Python Quickstart'

    @staticmethod
    def create_service():
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(GmailAPIUtil.CLIENT_SECRET_FILE, GmailAPIUtil.SCOPES)
            flow.user_agent = GmailAPIUtil.APPLICATION_NAME
            if GmailAPIUtil.flags:
                credentials = tools.run_flow(flow, store, GmailAPIUtil.flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)

        http = credentials.authorize(httplib2.Http())
        return discovery.build('gmail', 'v1', http=http)

    @staticmethod
    def compat_urlsafe_b64encode(v):
        """A urlsafe ba64encode which is compatible with Python 2 and 3.
        Args:
          v: A string to encode.
        Returns:
          The encoded string.
        """
        if sys.version_info[0] >= 3:  # pragma: NO COVER
            return base64.urlsafe_b64encode(v.encode('UTF-8')).decode('ascii')
        else:
            return base64.urlsafe_b64encode(v)

    @staticmethod
    def create_message(sender, to, subject, message_text):
        """Create a message for an email.
    
        Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
    
        Returns:
        An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': GmailAPIUtil.compat_urlsafe_b64encode(message.as_string())}

    @staticmethod
    def send_message(service, user_id, message):
        """Send an email message.
    
        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.
    
        Returns:
        Sent Message.
        """
        try:
            message = (service.users().messages().send(userId=user_id, body=message).execute())
            Logger.debug('Sent message {}'.format(message))
            return message
        except errors.HttpError as error:
            Logger.debug('An error occurred while sending message: %s' % error)
