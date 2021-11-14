import email
import base64

from email import policy
from email.iterators import _structure

fp = open("raw-mail.txt", "r")
msg = email.message_from_file(fp, policy=policy.default)

_structure(msg)

for part in msg.walk():
  if (part.get_content_type() == 'text/plain'):
    part.set_content('aaaa')
    print(part.get_content())
    # print(part.get_payload())
    # print(str(base64.urlsafe_b64decode(part.get_payload()), 'utf-8'))


# print(msg.get_body())

        # for h in msg['payload']['headers']:
        #     if h['name'] == 'Subject':
        #         new_msg['subject'] = Header(h['value'], 'utf-8').encode()
        #     if h['name'] == 'From':
        #         new_msg['from'] = h['value']
            
        # for part in msg['payload']['parts']:
        #     if part['filename'] == '' and part['mimeType'] == 'text/plain':
        #         if 'data' in part['body']:
        #             body = str(base64.urlsafe_b64decode(part['body']['data']), 'utf-8')
        #             new_msg.attach(MIMEText(body, 'plain', 'utf-8'))
        #     if part['filename'] == '' and part['mimeType'] == 'text/html':
        #         if 'data' in part['body']:
        #             body = str(base64.urlsafe_b64decode(part['body']['data']), 'utf-8')
        #             new_msg.attach(MIMEText(body, 'html', 'utf-8'))
        #     if part['filename']:
        #         if 'data' in part['body']:
        #             data = part['body']['data']
        #         else:
        #             att_id = part['body']['attachmentId']
        #             att = service.users().messages().attachments().get(userId=user_id, messageId=msg_id,id=att_id).execute()
        #             data = att['data']
        #         file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
        #         path = part['filename']


