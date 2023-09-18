import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from_addr='ENTER_SENDERS_MAILID'

data=pd.read_csv("abc.csv")         # Enter path of CSV files containing emails
to_addr=data['email'].tolist()      # Change'email' to column name containg emailids
name = data['name'].tolist()

l=len(name)
email=""   #Enter Your email id here
password=""           #Enter your Password

for i in range (l):
    msg=MIMEMultipart()
    msg['From']=from_addr
    msg['To']=to_addr[i]
    msg['Subject']='Just to Check'

    body=name[i]+'Enter your content here' 

    msg.attach(MIMEText(body,'plain'))

    mail=smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(email,password)
    text=msg.as_string()
    mail.sendmail(from_addr,to_addr[i],text)
    mail.quit()