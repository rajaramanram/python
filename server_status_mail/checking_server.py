from jinja2 import Environment,FileSystemLoader
from time_autointelli import total_date_time
#['anand@autointelli.com','ganesan.a@autointelli.com']
import paramiko
import smtplib
from subprocess import call
import subprocess
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
server_names=['10.227.45.103','10.227.45.104','10.227.45.105','10.227.45.106','10.227.45.107','10.227.45.108',
              '10.227.45.109','10.227.45.110','10.227.45.114','10.227.45.124','10.227.45.122','10.227.45.121',
              '10.227.45.123','10.227.45.119','10.227.45.120']
total_name=['autointellikvmmonitor\n', 'autointellisrv002\n', 'autointellisrv003\n',
            'autointellisrv004\n', 'autointellisrv005\n', 'autointellisrv006\n',
            'autointellisrv007\n', 'autointellisrv008\n', 'autointellisrv012\n',
            'autointellisrv018\n', 'autointellisr017\n', 'elasticsearchcls03\n',
            'autointellisrv019\n', 'elasticsearchcls01\n', 'elasticsearchcls02\n']
total_status=[['nagios is active (running)', 'mod-gearman-worker is active (running)'],
              ['mod-gearman-worker is active (running)'], ['nagios is active (running)','mod-gearman-worker is inactive (dead)'],
              ['nagios is active (running)', 'crond is active (running)'],
              ['mod-gearman-worker is active (running)'],['mod-gearman-worker is active (running)'],
              [], ['nagios is active (running)', 'mod-gearman-worker is active (running)'],
              ['postgresql-9.6 is active (running)', 'mongod is active (running)'],
              ['mariadb is active (running)'], ['rabbitmq-server is active (running)'], [], ['rabbitmq-server is active (running)'], [], []]
total_waiting=[[], [], ['4924 jobs waiting in service'], [], [], [], [], [],
               [], [], [], [], [], [], []]
'''for i,g in enumerate(server_names):
    for hell in total_status[i]:
        if hell.endswith("(running)"):
            print(hell)'''
port = 587 
smtp_server = "smtp.gmail.com"
login = "vmr.rajaraman@gmail.com"
password = 'raja3381'
sender_email = "vmr.rajaraman@gmail.com"
receiver_email = "vmr.raja99@gmail.com"
message = MIMEMultipart("alternative")
message["Subject"] = "sir"
message["From"] = sender_email
message["To"] = receiver_email
file_loader=FileSystemLoader('templates')
env=Environment(loader=file_loader)
template=env.get_template('final_server.html')
output=template.render(hostname=enumerate(server_names),servicename=total_name,total_list=total_status,
                       get_waiting_two=total_waiting,data_time=total_date_time)
part1 = MIMEText(output, "html")
message.attach(part1)
import smtplib
with smtplib.SMTP('smtp.gmail.com',587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(login,password)
    smtp.sendmail('vmr.rajaraman@gmail.com',receiver_email,message.as_string())



