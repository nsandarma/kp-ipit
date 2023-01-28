
from email.message import EmailMessage
import ssl
import smtplib

sec_pass = 'zpeusxkxbcvkwhxf'

email_sender = 'systeminformation51@gmail.com'
email_password = sec_pass

subject = "notif"

body = """
Hello world
"""

def send_notif(to,subject,body):
    for i in to:
        try:
            em = EmailMessage()
            em['From'] = 'Website Alumni Sistem Informasi'
            em['To'] = i
            em['subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smptp:
                smptp.login(email_sender,email_password)
                smptp.sendmail(email_sender,i,em.as_string())
            print('success')
        except :
            print('gagal')


sandy = [
    []
]



