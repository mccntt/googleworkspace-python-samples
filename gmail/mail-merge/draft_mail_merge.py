# -*- coding: utf-8 -*-
#
# Copyright ©2018-2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
docs-mail-merge.py (Python 2.x or 3.x)

Google Docs (REST) API mail-merge sample app
"""
# [START mail_merge_python]
from __future__ import print_function
import time

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

# Fill-in IDs of your Docs template & any Sheets data source
SHEETS_FILE_ID = '1zAmLQWZclO-picIy6kQdw1XMIGEOUXcNKCPqyX0R2cY'
DRAFT_SUBJECT = '最后通知：您的Google Workspace工作账号即将迁移到新的Google Workspace平台'

# authorization constants
CLIENT_ID_FILE = '/Users/fangchih/Dropbox/devkey/client_secret_480714232090-i4uvmjv4nmevt0ac24rninmod5ijgc6i.apps.googleusercontent.com.json'
TOKEN_STORE_FILE = 'token.json'
SCOPES = (  # iterable or space-delimited string
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
)

# application constants
SOURCE = 'sheets' # Choose one of the data SOURCES
COLUMNS = ['to_name', 'to_title', 'to_company', 'to_address']


def get_http_client():
    """Uses project credentials in CLIENT_ID_FILE along with requested OAuth2
        scopes for authorization, and caches API tokens in TOKEN_STORE_FILE.
    """
    store = file.Storage(TOKEN_STORE_FILE)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_ID_FILE, SCOPES)
        creds = tools.run_flow(flow, store)
    return creds.authorize(Http())


# service endpoints to Google APIs
HTTP = get_http_client()
DRIVE = discovery.build('drive', 'v3', http=HTTP)
DOCS = discovery.build('docs', 'v1', http=HTTP)
SHEETS = discovery.build('sheets', 'v4', http=HTTP)
GMAIL = discovery.build('gmail', 'v1', http=HTTP)


def _get_sheets_data(service=SHEETS):
    """(private) Returns data from Google Sheets source. It gets all rows of
        'Sheet1' (the default Sheet in a new spreadsheet), but drops the first
        (header) row. Use any desired data range (in standard A1 notation).
    """
    ssvalues = service.spreadsheets().values().get(spreadsheetId=SHEETS_FILE_ID,
            range='Sheet1').execute().get('values')
    global COLUMNS
    COLUMNS = ssvalues[0]
    return ssvalues[1:] # skip header row


def gen_token():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_STORE_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_STORE_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_ID_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        # with open(TOKEN_STORE_FILE, 'w') as token:
        #     token.write(creds.to_json())


    def getGmailTemplateFromDrafts_(subject_line):
        """
        Get a Gmail draft message by matching the subject line.
        @param {string} subject_line to search for draft message
        @return {object} containing the subject, plain and html message body and attachments
        """
        try:
            // get drafts
            const drafts = GmailApp.getDrafts();
            // filter the drafts that match subject line
            const draft = drafts.filter(subjectFilter_(subject_line))[0];
            // get the message object
            const msg = draft.getMessage();

            // Handling inline images and attachments so they can be included in the merge
            // Based on https://stackoverflow.com/a/65813881/1027723
            // Get all attachments and inline image attachments
            const allInlineImages = draft.getMessage().getAttachments({includeInlineImages: true,includeAttachments:false});
            const attachments = draft.getMessage().getAttachments({includeInlineImages: false});
            const htmlBody = msg.getBody(); 

            // Create an inline image object with the image name as key 
            // (can't rely on image index as array based on insert order)
            const img_obj = allInlineImages.reduce((obj, i) => (obj[i.getName()] = i, obj) ,{});

            //Regexp to search for all img string positions with cid
            const imgexp = RegExp('<img.*?src="cid:(.*?)".*?alt="(.*?)"[^\>]+>', 'g');
            const matches = [...htmlBody.matchAll(imgexp)];

            //Initiate the allInlineImages object
            const inlineImagesObj = {};
            // built an inlineImagesObj from inline image matches
            matches.forEach(match => inlineImagesObj[match[1]] = img_obj[match[2]]);

            return {message: {subject: subject_line, text: msg.getPlainBody(), html:htmlBody}, 
                    attachments: attachments, inlineImages: inlineImagesObj };
        except Exception as e:
            throw new Error("Oops - can't find Gmail draft");

        /**
            * Filter draft objects with the matching subject linemessage by matching the subject line.
            * @param {string} subject_line to search for draft message
            * @return {object} GmailDraft object
        */
        function subjectFilter_(subject_line){
            return function(element) {
            if (element.getMessage().getSubject() === subject_line) {
                return element;
            }
            }
        }
  


if __name__ == '__main__':

    gen_token()

    # fill-in your data to merge into document template variables
    merge = {}

    # get row data, then loop through & process each form letter
    data = get_data(SOURCE) # get data from data source
    for i, row in enumerate(data):
        merge.update(dict(zip(COLUMNS, row)))
        print(merge)
        print('Merged letter %d: docs.google.com/document/d/%s/edit' % (
                i+1, merge_template(DOCS_FILE_ID, SOURCE, DRIVE)))
# [END mail_merge_python]
