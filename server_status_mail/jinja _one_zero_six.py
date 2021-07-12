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
server_names=['10.227.45.103','10.227.45.104','10.227.45.105','10.227.45.106','10.227.45.110']
port='10.227.45.121'
user_name='root'
pass_word='@ut0!ntell!@234'
service_names=['Nagios','Gearmand','pnp-gearman-worker','npcd']

ssh_client = paramiko.SSHClient()
ssh_client.load_system_host_keys()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=port,username=user_name,password=pass_word)
#cmd='hostname'
status=[]
stdin, stdout, stderr = ssh_client.exec_command("hostname ; systemctl status rabbitmq-server ; ps -ef|grep elasticsearch.bootstrap|grep -v grep")
get_service=stdout.readlines()
print(get_service)
for line in get_service:
    if line.startswith("autoint+"):
        slice_line=line[:80]
        print(slice_line)
        res = " ".join(slice_line.split())
        print(res)
        status.append(res)
        print(status)


        

'''stri='autoint+  22563      1 21 Oct01 ?        2-11:40:01 /var/analytics/jdk/bin/java'
length_string=len(stri)
print(length_string)
res = " ".join(stri.split())
print(res)'''
print(type(res))
print(str(res))
