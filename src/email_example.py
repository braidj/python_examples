#!/usr/bin/python3 env
import os
import smtplib
import mimetypes
from email.message import EmailMessage

script = os.path.basename(__file__)

message = EmailMessage()

sender = 'braidj@gmail.com'
recipient = "braidj@gmail.com"
message['from'] = sender
message['to'] = recipient
message['Subject'] = f"Greetings from {sender} via {script}"

body = """Light weight example of sending an email from my google account
Including an attachment"""

message.set_content(body)

# Add attachment details
attachment_path = f"{os.curdir}/images/bladerunner2.png"
mime_type, _ = mimetypes.guess_type(attachment_path)
mime_type, mime_subtype = mime_type.split('/', 1)

with open(attachment_path, 'rb') as ap:
    message.add_attachment(ap.read(),
                           maintype=mime_type,
                           subtype=mime_subtype,
                           filename="bladerunner2.png")

try:
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    mail_server.login("braidj@gmail.com", 'edinbkpdkcvdnjml')
    no_send_recipients = mail_server.send_message(message)

    if len(no_send_recipients):
        print("Warninging {} recipients did not receive the message".format(
            len(no_send_recipients)))

    mail_server.quit()
    print("Email sent")

except Exception as e:
    print(f"ERROR has occurred \n{e}")
