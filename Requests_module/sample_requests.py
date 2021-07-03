import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment,FileSystemLoader
import requests
with open("url_list_main.csv",'r')as read_file:
    get_url = read_file.read().splitlines()
    print(get_url)
print(get_url)
email_list=['vmr.raja99@gmail.com']
#email_list=['anand@autointelli.com','ganesan.a@autointelli.com','dinesh@autointelli.com']
#get_url=['https://r2d2.nxtgen.com', 'https://r2d2.nxtgen.com/nxtgen', 'https://61.0.172.106/', 'https://117.255.216.170/']
get_response=[]
get_response_time=[]

for i in get_url:
    try:
        r=requests.get(i,verify=False)
        get_response.append(r.status_code)
        get_response_time_format=format(r.elapsed.total_seconds(),'.2f')
        get_response_time.append(get_response_time_format)
    except requests.exceptions.RequestException as e:
        get_exception=e
        print(get_exception)
        get_response.append(get_exception)
        pass

print(get_response)
print(get_response_time)

port = 587
smtp_server = "smtp.gmail.com"
login = "vmr.rajaraman@gmail.com"
password = 'raja3381'
sender_email = "vmr.rajaraman@gmail.com"
receiver_email = email_list
message = MIMEMultipart("alternative")
message["Subject"] = "sir,URL response checking"
message["From"] = sender_email
message["To"] = ",".join(receiver_email)
file_loader=FileSystemLoader('templates')
env=Environment(loader=file_loader)
template=env.get_template('requests_temp.html')
#,user_name=payload['username'],pass_word=payload['password']
output=template.render(final_url=enumerate(get_url),get_response=get_response,get_response_time=get_response_time)
part1 = MIMEText(output, "html")
message.attach(part1)
        
with smtplib.SMTP('smtp.gmail.com',587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(login,password)
    smtp.sendmail('vmr.rajaraman@gmail.com',receiver_email,message.as_string())
'''payload={'username':'user','password':'testing'}
for i in get_url:
    r=requests.get(i)
    get_response=r.status_code
    print(get_response)
    get_response_time=format(r.elapsed.total_seconds(),'.1f')
    print(get_response_time)'''
'''url_list=['https://r2d2.nxtgen.com\n','https://r2d2.nxtgen.com/nxtgen\n','https://61.0.172.106/\n','https://117.255.216.170/']
with open("url_list_main.csv",'w')as file:
    for i in url_list:
        file.write(i)'''
      

    
    

