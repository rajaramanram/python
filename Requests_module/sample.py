
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment,FileSystemLoader
port = 587 
smtp_server = "smtp.gmail.com"
login = "vmr.rajaraman@gmail.com"
password = 'raja3381'
sender_email = "vmr.rajaraman@gmail.com"
receiver_email = 'vmr.raja99@gmail.com'
message = MIMEMultipart("alternative")
message["Subject"] = "s"
message["From"] = sender_email
message["To"] = receiver_email
file_loader=FileSystemLoader('templates')
env=Environment(loader=file_loader)
template=env.get_template('requests_temp.html')
output=template.render(final_url=get_url[0],user_name=payload['username'],pass_word=payload['password'],
                           get_response=get_response,get_response_time=get_response_time)
part1 = MIMEText(output, "html")
message.attach(part1)
    
with smtplib.SMTP('smtp.gmail.com',587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(login,password)
    smtp.sendmail('vmr.rajaraman@gmail.com',receiver_email,message.as_string())

    
    
