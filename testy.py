import smtplib       
try:
    content = 'test'

    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()
    mail.starttls()
    mail.login("zontick99@gmail.com", "ydgwprmfajkliynw")
    mail.sendmail("zontick99@gmail.com", "sasha.oom7@gmail.com", content)
    mail.quit
    print("Successfully sent email")
except smtplib.SMTPException:
    print ("error")