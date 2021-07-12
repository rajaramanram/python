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
server_names=['10.227.45.103','10.227.45.104','10.227.45.105','10.227.45.106','10.227.45.107','10.227.45.108',
              '10.227.45.109','10.227.45.110','10.227.45.114','10.227.45.124','10.227.45.122','10.227.45.121',
              '10.227.45.123','10.227.45.119','10.227.45.120']
service_string=''
html_service=[]
service_regx = r"Loaded:.*\/(.*service);"
status_regx= r"Active:(.*) since (.*);(.*)"
user_name='root'
pass_word='@ut0!ntell!@234'
total_server=[]
total_name=[]
total_status=[]
total_waiting=[]
for select_port in server_names:
    port=select_port
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=port,username=user_name,password=pass_word)
    dict_server={
    '10.227.45.103':"hostname ; systemctl status nagios ; systemctl status mod-gearman-worker",
    '10.227.45.104':"hostname ; systemctl status mod-gearman-worker",
    '10.227.45.105':"hostname ; systemctl status nagios ; systemctl status mod-gearman-worker",
    '10.227.45.106':"hostname ; systemctl status nagios ; systemctl status crond",
    '10.227.45.107':"hostname ; systemctl status mod-gearman-worker",
    '10.227.45.108':"hostname ; systemctl status mod-gearman-worker",
    '10.227.45.109':"hostname ; systemctl status mod-gearman-worker",
    '10.227.45.110':"hostname ; systemctl status nagios ; systemctl status mod-gearman-worker",
    '10.227.45.114':"hostname ; systemctl status postgresql-9.6 ; systemctl status mongod",
    '10.227.45.124':"hostname ; systemctl status mariadb",
    '10.227.45.122':"hostname ; systemctl status nfsd ; systemctl status rabbitmq-server",
    '10.227.45.121':"hostname ; systemctl status rabbitmq-server ; ps -ef|grep elasticsearch.bootstrap|grep -v grep",
    '10.227.45.123':"hostname ; systemctl status rabbitmq-server",
    '10.227.45.119':"hostname ; service kibana status ; ps -ef|grep elasticsearch.bootstrap|grep -v grep",
    '10.227.45.120':"hostname ; ps -ef|grep elasticsearch.bootstrap|grep -v grep",
    }.get(select_port)
    cmd=str(dict_server)
    #cmd="hostname ; systemctl status nagios ; systemctl status mod-gearman-worker ; systemctl status crond"
    #stdin, stdout, stderr = ssh_client.exec_command("hostname ; systemctl status nagios ;")
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    get_service=stdout.readlines()
    service_name=[]
    service_status=[]
    worker_name=get_service[0]
    total_name.append(worker_name)
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
            
        elif line.endswith("running\n"):
            line_remove=line.rstrip()
            #print(line_remove)
            line_remove2=[line_remove]

            #total_status.append(line_remove2)
        elif line.startswith("autoint+"):
            if port == '10.227.45.119':
                slice_line=line[:80]
                res = " ".join(slice_line.split())
                list_res=[res]
                line_remove2.extend(list_res)
                total_status.append(line_remove2)
            else:
                slice_line=line[:80]
                res = " ".join(slice_line.split())
                #print(res)
                list_res=[res]
                #print(list_res)
                total_status.append(list_res)
            

    #print(service_name)
    #print(service_status)
    total_list = [(service_name[i] +' is '+ service_status[i]) for i in range(len(service_name))]
    if port != '10.227.45.121' and port != '10.227.45.119' and port != '10.227.45.120':
        total_status.append(total_list)
    #print(total_status)
    stdin, stdout, stderr = ssh_client.exec_command("gearman_top -b")
    get_service2=stdout.read().splitlines()
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
    #print(split_list)
    get_waiting=[]    
    #li=[['eventhandler', '77', '1002', '0'],['eventha', '77', '0', '0'],['evdler', '77', '1234', '0']]
    for i in split_list[1:]:
        if int(i[2])>= 1000:
            statement=str(i[2])+' jobs waiting in '+i[0]
            #print(statement)
            get_waiting.append(statement)
    #print(get_waiting)
    total_waiting.append(get_waiting)
#print(total_name)
#print(total_status)
#print(total_waiting)
port = 587 
smtp_server = "smtp.gmail.com"
login = "vmr.rajaraman@gmail.com"
password = 'raja3381'
sender_email = "vmr.rajaraman@gmail.com"
receiver_email = 'anand@autointelli.com'
message = MIMEMultipart("alternative")
message["Subject"] = "sir,i did changes,in 119 also did elastic search command,please check sir"
message["From"] = sender_email
message["To"] = receiver_email
file_loader=FileSystemLoader('templates')
env=Environment(loader=file_loader)
template=env.get_template('one_table.html')
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



