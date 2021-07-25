# Python 3.8.0
import smtplib
import time
import imaplib
import email
import traceback
import email
from email.header import decode_header
import webbrowser
import os
import smtplib
import asyncio

import sched, time
s = sched.scheduler(time.time, time.sleep)

body = "h"
ORG_EMAIL = "@gmail.com" 
FROM_EMAIL = "vihesh.duha.offcl" + ORG_EMAIL 
FROM_PWD = "5175cb85" 
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993
email_text = """\
Subject:'OMG Super Important Message'

This message is sent from Python."""
def send_email_to_new_emails(email_1):
    print("triggered4")
    to = email_1

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(FROM_EMAIL, FROM_PWD)
        server.sendmail(FROM_EMAIL, to, email_text)
        server.close()

        print ('Email sent!')
    except:
        print ('Something went wrong...')

async def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')
        reetcode , data = mail.search(None, 'UnSeen')

        if reetcode == 'OK':
            mail_ids = data
            id_list = mail_ids[0].split()
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])
            for i in range(latest_email_id, first_email_id-1, -1):
                res, msg = mail.fetch(str(i), "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        # parse a bytes email into a message object
                        msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    name, email_id = email.utils.parseaddr(msg.get("From"))
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    # if the email message is multipart
                    if msg.is_multipart():
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                try:
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    pass
                    else:
                        content_type = msg.get_content_type()
                        if content_type == "text/plain":
                            body = msg.get_payload(decode=True).decode()

                    body_without = str(body.replace("\n", ""))
                    body_without = body_without.strip()
                    if body_without == "imreallytiredthisdaysucks":
                        print("triggered1")
                        send_email_to_new_emails(email_id)
                    else:
                        print("do not match")
                    
                    print("Subject:", subject)
                    print("From:", email_id)
                    print(body_without)
                    print("="*100)
        mail.close()
        mail.logout()

    except Exception as e:
        traceback.print_exc() 
        print(str(e))
async def call_others():
    while True:
        await read_email_from_gmail()

loop = asyncio.get_event_loop()
loop.create_task(call_others())
loop.run_forever()