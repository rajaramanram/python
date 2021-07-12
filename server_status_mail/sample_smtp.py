#import the smtplib module. It should be included in Python by default
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# set up the SMTP server
s = smtplib.SMTP(host='209.133.209.251', port=587)
s.starttls()
s.login('vmr.rajaraman@gmail.com','raja3381')
name='raja'
message='sniper master'
e_mail='vmr.raja99@gmail.com'
msg = MIMEMultipart()       # create a message
# add in the actual person name to the message template
#message = message_template.substitute(PERSON_NAME=name.title())

# setup the parameters of the message
msg['From']='vmr.rajaraman@gmail.com'
msg['To']=e_mail
msg['Subject']="This is TEST"

# add in the message body
msg.attach(MIMEText(message, 'plain'))

# send the message via the server set up earlier.
s.send_message(msg)
s.quit()
