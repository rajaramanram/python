#!/usr/bin/env python3
from  jinja2 import Template
from time_autointelli import total_date_time
#['anand@autointelli.com','ganesan.a@autointelli.com']
import paramiko
import smtplib
from subprocess import call
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port='172.16.1.102'
user_name='root'
pass_word='Wigtra@devserver1'
server_names=['10.227.45.103','10.227.45.105','10.227.45.106','10.227.45.110']
service_names=['Nagios','Gearmand','pnp-gearman-worker','npcd']

ssh_client = paramiko.SSHClient()
ssh_client.load_system_host_keys()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=port,username=user_name,password=pass_word)
#cmd='hostname'

stdin, stdout, stderr = ssh_client.exec_command("hostname \n service --status-all")
get_service=stdout.readlines()
print(get_service)
service_string=''
#print(get_service[-2:])
html_service=[]
'''for i in get_service[-2:]:
    html_service+=i
print(html_service)
for i in get_service:
    for y in service_names:
        #print(get_service)
        #print(y)
        if i.startswith(y) and i.endswith("is running...\n"):
            html_service+=i
            print(html_service)'''
for i in get_service:       
    if i.endswith("running...\n") or i.endswith("running\n"):
        html_service.append(i)
print(html_service)
'''for i in get_service:
    service_string=(service_string+'\n'+str(i.encode()))
print(service_string)'''
port = 587 
smtp_server = "smtp.gmail.com"
login = "vmr.rajaraman@gmail.com"
password = 'raja3381'
sender_email = "vmr.rajaraman@gmail.com"
receiver_email = 'vmr.raja99@gmail.com'
message = MIMEMultipart("alternative")
message["Subject"] = "sir,i used service name for selecting multiple service which is running,previous model i used indexing sir,please tell changes sir"
message["From"] = sender_email
message["To"] = receiver_email
hostname='172.16.1.102'
service_name=get_service[0]
print(service_name)
html=f"""\
<html>
    <body>
        <br>
        <center><b>Service Notification Manager</b></center>
        <br*2>
        <h3><b>Summary</b></h3>
        <hr style="widows: 100px;" >
        <p>service Status information on Host {hostname} for Service - {service_name}</p>
        <br*2>
        <h3><b>Alert Details:</b></h3>
        <br*2>
        <h3><b></b></h3>
        <TABLE BORDER="4"    WIDTH="50%"   CELLPADDING="5" CELLSPACING="3">
        
            <TR>
                <TD>Notification</TD>
                <TD>Service Restart</TD>
            </TR>
            
            <TR>
                <TD>Host Name</TD>
                <TD>{hostname}</TD>
            </TR>
            <TR>
                <TD>Service Description</TD>
                <TD>{html_service}</TD>
            </TR>
            </TR>
            <TR>
                <TD>Time</TD>
                <TD>{total_date_time}</TD>
            </TR>
        </TABLE>
        <br*3>
        <h4><b>Regards,</b></h4>
        <h4>Autointelli</h4>
    </body>
</html>"""
part1 = MIMEText(html, "html")
message.attach(part1)
import smtplib
with smtplib.SMTP('smtp.gmail.com',587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(login,password)
    #subject='172.16.1.102 service status'
    #body=service_string
    #msg=f'Subject:{subject}\n\n\n{body}'
    #message.as_string()
    smtp.sendmail('vmr.rajaraman@gmail.com',receiver_email,message.as_string())

    




