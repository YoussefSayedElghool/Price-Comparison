import smtplib, ssl
import json

with open('config.json', 'r') as file:
    data = json.load(file)

port = 587 
smtp_server = data["smtp_server"]
sender_email = data["sender_email"]
password = data["password"]


def sende_email(message , receiver_email):
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  
        server.starttls(context=context)
        server.ehlo() 
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


sende_email("Bala7 hi" , "www33868242@gmail.com")