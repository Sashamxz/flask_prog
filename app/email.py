import smtplib
from threading import Thread
from flask import current_app
from flask_mail import Message
from main import app


mail = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])




def send_async_email(app, msg):
    with app.app_context():
        mail.sendmail(msg)


def send_email(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=False):
    try:
        mail.ehlo()
        mail.starttls()
        mail.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])           
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        if attachments:
            for attachment in attachments:
                msg.attach(*attachment)
        if sync:
            mail.sendmail(msg)
        else:
            Thread(target=send_async_email,
                args=(current_app._get_current_object(), msg)).start()
        
        mail.quit        

    except smtplib.SMTPException: 
        print('f{error}')