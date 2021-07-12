import smtplib
with smtplib.SMTP('smtp.gmail.com',587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login('vmr.rajaraman@gmail.com','raja3381')
    subject='abcede'
    body='12345'
    msg=f'Subject:{subject}\n\n\n{body}'
    smtp.sendmail('vmr.rajaraman@gmail.com','vmr.raja99@gmail.com',msg)
