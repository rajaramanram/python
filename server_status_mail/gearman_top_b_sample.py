from jinja2 import Environment,FileSystemLoader
from time_autointelli import total_date_time
#['anand@autointelli.com','ganesan.a@autointelli.com']
import paramiko
import smtplib
from subprocess import call
import subprocess
import re
import csv
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
    
