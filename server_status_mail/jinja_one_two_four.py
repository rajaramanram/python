'''#https://github.com/torfsen/python-systemd-tutorial
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
server_names=['10.227.45.121','10.227.45.120']
port='10.227.45.120'
user_name='root'
pass_word='@ut0!ntell!@234'
ssh_client = paramiko.SSHClient()
ssh_client.load_system_host_keys()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=port,username=user_name,password=pass_word)
#cmd='hostname'

stdin, stdout, stderr = ssh_client.exec_command("hostname ; ps -ef|grep elasticsearch.bootstrap|grep -v grep")
get_service=stdout.readlines()
print(get_service)'''
st='autoint+  22563      1 21 Oct01 ?        2-08:37:24 /var/analytics/jdk/bin/java'
#st_remove=st.strip()
#print(st_remove)
