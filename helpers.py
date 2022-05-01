from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
import csv
import olx.constants as const
from dotenv import load_dotenv
import os

load_dotenv()

def dictlist_to_csv(file_name,dictlist,fields):
    '''convert list of dictionaries to a csv file'''
    with open(f'{file_name}.csv', 'w', encoding="utf-8-sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writeheader()
        writer.writerows(dictlist)



def send_mail(email_to):
    '''sends mail to a specified email'''
    # Create a multipart message
    msg = MIMEMultipart()
    body_part = MIMEText(const.MESSAGE_BODY, 'plain')
    msg['Subject'] = const.EMAIL_SUBJECT
    msg['From'] = formataddr(("Olx Scraper",const.EMAIL_FROM))
    msg['To'] = email_to
    # Add body to email
    msg.attach(body_part)
    # open and read the CSV file in binary
    with open('items.csv','rb') as file:
    # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name="items.csv"))

    # Create SMTP object
    smtp_obj = smtplib.SMTP(const.EMAIL_HOST, const.SMTP_PORT)
    smtp_obj.starttls()
    # Login to the server
    smtp_obj.login(const.EMAIL_FROM, os.environ.get("EMAIL_PASSWORD"))

    # Convert the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp_obj.quit()