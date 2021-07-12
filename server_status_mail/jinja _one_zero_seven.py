#https://github.com/torfsen/python-systemd-tutorial
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
server_names=['10.227.45.103','10.227.45.104','10.227.45.105','10.227.45.106','10.227.45.107','10.227.45.110']
port='10.227.45.119'
user_name='root'
pass_word='@ut0!ntell!@234'
service_names=['Nagios','Gearmand','pnp-gearman-worker','npcd']

ssh_client = paramiko.SSHClient()
ssh_client.load_system_host_keys()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=port,username=user_name,password=pass_word)
#cmd='hostname'

stdin, stdout, stderr = ssh_client.exec_command("hostname ; service kibana status")
get_service=stdout.readlines()
print(get_service)

service_string=''
html_service=[]
service_regx = r"Loaded:.*\/(.*service);"
status_regx= r"Active:(.*) since (.*);(.*)"
#using list
service_name=[]
service_status=[]
for line in get_service:
    #print(line.endswith("running\n"))
    #print(line)
    service_search = re.search(service_regx, line)
    status_search = re.search(status_regx, line)
    if service_search :
            service_name.append(service_search.group(1).replace(".service",''))
    
    elif status_search:
            service_status.append(status_search.group(1).strip())
    elif line.endswith("running\n"):
        line_remove=line.rstrip()
        print(line_remove)
        service_name.append(line_remove)
print(service_name)
print(service_status)
total_list=[]
for i in service_name:
    for y in service_status:
        ans=i+' is '+y
        #print(ans)
        total_list.append(ans)
        break
print(total_list)
'''port = 587 
smtp_server = "smtp.gmail.com"
login = "vmr.rajaraman@gmail.com"
password = 'raja3381'
sender_email = "vmr.rajaraman@gmail.com"
receiver_email = 'vmr.raja99@gmail.com'
message = MIMEMultipart("alternative")
message["Subject"] = "sir,"
message["From"] = sender_email
message["To"] = receiver_email
hostname=server_names[4]
service_name=get_service[0]
print(service_name)
file_loader=FileSystemLoader('templates')
env=Environment(loader=file_loader)
template=env.get_template('one_zero_three.html')
output=template.render(hostname=hostname,servicename=service_name,total_list=total_list,data_time=total_date_time)
#print(output)
part1 = MIMEText(output, "html")
message.attach(part1)
import smtplib
with smtplib.SMTP('smtp.gmail.com',587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(login,password)
    smtp.sendmail('vmr.rajaraman@gmail.com',receiver_email,message.as_string())'''
