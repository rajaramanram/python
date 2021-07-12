from jinja2 import Environment,FileSystemLoader
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
    if i.endswith("running...\n") or i.endswith("running\n") or i.endswith("running.\n"):
        html_service.append(i)
print(html_service)
'''for i in get_service:
    service_string=(service_string+'\n'+str(i.encode()))
print(service_string)'''
for multi_service in range(len(html_service)):
    print(multi_service)
    insert_service=html_service[multi_service]
    print(insert_service)
    port = 587 
    smtp_server = "smtp.gmail.com"
    login = "vmr.rajaraman@gmail.com"
    password = 'raja3381'
    sender_email = "vmr.rajaraman@gmail.com"
    receiver_email = 'ganesan.a@autointelli.com'
    message = MIMEMultipart("alternative")
    message["Subject"] = "sir,separte emails for multiple service,please check sir "
    message["From"] = sender_email
    message["To"] = receiver_email
    hostname='172.16.1.102'
    service_name=get_service[0]
    print(service_name)
    file_loader=FileSystemLoader('templates')
    env=Environment(loader=file_loader)
    template=env.get_template('status_email2.html')
    output=template.render(hostname=hostname,servicename=service_name,ht_service= insert_service,data_time=total_date_time)
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
