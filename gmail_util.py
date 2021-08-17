import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config
from smtplib import SMTPAuthenticationError


def send_email(subject, msg, email_address):
    try:
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = config.EMAIL_ADDRESS
        message['To'] = email_address
        html = MIMEText(msg, 'html')
        message.attach(html)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        server.sendmail(config.EMAIL_ADDRESS, email_address, message.as_string())
        server.quit()
        print(f"Email send successfully to {email_address}")
    except SMTPAuthenticationError as e:
        print("Could not send email because there was an error with the authentication "
              "(Maybe you need to allow less secure apps to your account), see message below:\n")
        print(e)
    except:
        print("Error while trying to send email")
