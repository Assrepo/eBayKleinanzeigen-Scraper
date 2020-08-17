import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config


def send_email(subject, msg, email_addrress):
    try:
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = config.EMAIL_ADDRESS
        message['To'] = email_addrress
        html = MIMEText(msg, 'html')
        message.attach(html)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        server.sendmail(config.EMAIL_ADDRESS, email_addrress, message.as_string())
        server.quit()
        print("Messege send succesfully")
    except:
        print("Error while trying to send email")
