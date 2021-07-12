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
server_names=['10.227.45.103','10.227.45.105','10.227.45.106','10.227.45.110']
port=server_names[0]
user_name='root'
pass_word='@ut0!ntell!@234'
service_names=['Nagios','Gearmand','pnp-gearman-worker','npcd']

ssh_client = paramiko.SSHClient()
ssh_client.load_system_host_keys()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=port,username=user_name,password=pass_word)
#cmd='hostname'

stdin, stdout, stderr = ssh_client.exec_command("hostname ; systemctl status nagios ; systemctl status mod-gearman-worker")
get_service=stdout.readlines()
service_string=''
html_service=[]
service_regx = r"Loaded:.*\/(.*service);"
status_regx= r"Active:(.*) since (.*);(.*)"
#service_status = {}
#using list
service_name=[]
service_status=[]
for line in get_service:
    #print(line)
    service_search = re.search(service_regx, line)
    status_search = re.search(status_regx, line)
    if service_search:
            #service_status['service'] = service_search.group(1)
            #print("service:", service)
            service_name.append(service_search.group(1).replace(".service",''))

    elif status_search:
            #service_status['status'] = status_search.group(1).strip()
            service_status.append(status_search.group(1).strip())
            #print("status:", status.strip())
            #service_status['since'] = status_search.group(2).strip()
            #print("since:", since.strip())
            #service_status['uptime'] = status_search.group(3).strip()
            #print("uptime:", uptime.strip())
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
stdin, stdout, stderr = ssh_client.exec_command("gearman_top -b")
get_service2=stdout.read().splitlines()
#get_service3=get_service2.decode()
#print(get_service2)
get_top=[]
get_total=[]
for i in get_service2[2:]:
    i=i.decode()
    if not(i.startswith("-----")):
        change_i=i.replace("|",",")
        change_split=change_i.split(",")
        for y in change_split:
            change_space=y.strip()
            get_top.append(change_space)
        #get_total.append(get_top)
split_list= [get_top[y:y+4] for y in range(0,len(get_top),4)]
#print(get_top)
#print(get_total)           
print(split_list)
get_waiting=[]
#li=[['eventhandler', '77', '1002', '0'],['eventha', '77', '0', '0'],['evdler', '77', '1234', '0']]
for i in split_list[1:]:
    if int(i[2])>= 1000:
        statement=str(i[2])+' jobs waiting in '+i[0]
        print(statement)
        get_waiting.append(statement)
#print(get_waiting)        

port = 587 
smtp_server = "smtp.gmail.com"
login = "vmr.rajaraman@gmail.com"
password = 'raja3381'
sender_email = "vmr.rajaraman@gmail.com"
receiver_email = 'ganesan.a@autointelli.com'
message = MIMEMultipart("alternative")
message["Subject"] = """sir,i did,if jobs waiting(1000)or more in gearman_top it will create row and show the Queue
                    Name and number of jobs waiting in table,please tell next task sir"""
message["From"] = sender_email
message["To"] = receiver_email
hostname=server_names[0]
worker_name=get_service[0]
print(service_name)
file_loader=FileSystemLoader('templates')
env=Environment(loader=file_loader)
template=env.get_template('one_zero_three.html')
output=template.render(hostname=hostname,servicename=worker_name,total_list=total_list,data_time=total_date_time)
#print(output)
part1 = MIMEText(output, "html")
message.attach(part1)
import smtplib
with smtplib.SMTP('smtp.gmail.com',587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(login,password)
    smtp.sendmail('vmr.rajaraman@gmail.com',receiver_email,message.as_string())
