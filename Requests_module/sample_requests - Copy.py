import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment,FileSystemLoader
import requests
url_list=['https://r2d2.nxtgen.com\n','https://r2d2.nxtgen.com/nxtgen\n','https://61.0.172.106/\n','https://117.255.216.170/']
with open("url_list_main.csv",'w')as file:
    for i in url_list:
        file.write(i)
      
    
with open("url_list_main.csv",'r')as read_file:
    get_url = read_file.read().splitlines()
    print(get_url)
print(type(get_url))
for i in get_url:
    r=requests.get(i,verify=False)
    get_response=r.status_code
    print(get_response)
    get_response_time=format(r.elapsed.total_seconds(),'.2f')
    print(get_response_time)

email_list=['vmr.raja99@gmail.com']
#email_list=['anand@autointelli.com','ganesan.a@autointelli.com']
'''#payload={'username':'user','password':'testing'}
#r=requests.post("https://www.google.com",data=payload)
r=requests.get("https://www.google.com")
#r=requests.get("https://www.google.com/user/testing",auth=('user','testing'))
get_response=r.status_code
get_response_time=r.elapsed.total_seconds()
print(get_response_time)
#print(r.text)               
#r_dict=r.json()
#get_json_form=r_dict['form']
#print(get_json_form)'''
'''payload={'username':'user','password':'testing'}
get_url=["https://www.google.com"]
for i in get_url:
    r=requests.get(i)
    get_response=r.status_code
    get_response_time=format(r.elapsed.total_seconds(),'.1f')
    print(get_response_time)

for e in email_list:
    port = 587 
    smtp_server = "smtp.gmail.com"
    login = "vmr.rajaraman@gmail.com"
    password = 'raja3381'
    sender_email = "vmr.rajaraman@gmail.com"
    receiver_email = e
    message = MIMEMultipart("alternative")
    message["Subject"] = "sir,please check and give suggestion(outputs) to add in table"
    message["From"] = sender_email
    message["To"] = receiver_email
    file_loader=FileSystemLoader('templates')
    env=Environment(loader=file_loader)
    template=env.get_template('requests_temp.html')
    output=template.render(final_url=get_url[0],user_name=payload['username'],pass_word=payload['password'],
                               get_response=get_response,get_response_time=get_response_time)
    part1 = MIMEText(output, "html")
    message.attach(part1)
        
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(login,password)
        smtp.sendmail('vmr.rajaraman@gmail.com',receiver_email,message.as_string())'''

    
    

