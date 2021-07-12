import paramiko
#smtplib-simple mail trainsfer protcol library is used to send mail.
import smtplib
from subprocess import call
import subprocess

port='172.16.1.102'
user_name='root'
pass_word='Wigtra@devserver1'
server_names=['10.227.45.103','10.227.45.105','10.227.45.106','10.227.45.110']
service_names=['Nagios','Gearmand','Mod-gearman-worker','Npcd']

'''create SSHClient instance from paramkio module
SSH-Security procedure-to make secure connection between two computers'''
ssh_client = paramiko.SSHClient()
ssh_client.load_system_host_keys()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=port,username=user_name,password=pass_word)
cmd='service --status-all'

'''standard streams-for executing the commands
stdin-standard input
stdout-is used by the program to send data
stderr=standard error - to write errors in program'''
stdin, stdout, stderr = ssh_client.exec_command(cmd)
get_service=stdout.readlines()
print(get_service)
service_string=''
for i in get_service:
    service_string=(service_string+'\n'+str(i.encode()))
print(service_string)
    
import smtplib
with smtplib.SMTP('smtp.gmail.com',587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login('vmr.rajaraman@gmail.com')
    subject='172.16.1.102 service status'
    body=service_string
    msg=f'Subject:{subject}\n\n\n{body}'
    smtp.sendmail('vmr.rajaraman@gmail.com','ganesan.a@autointelli.com',msg)
#list_service=get_service[-8]
#print("\nservice name=",list_service)

'''#command = raw_input('Please enter service name : ')
command=list_service
status=call(["/etc/init.d/"+command, "status"])
print(status)'''
'''p =  subprocess.Popen(["root@aidevsrv002","service --status-all"], stdout=subprocess.PIPE)
print(p)
(output, err) = p.communicate()
output = output.decode('utf-8')

print(output)'''

