import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
import csv

config = configparser.ConfigParser()
config.read('config.ini')

sender_email = config['Sender']['sender_email']
sender_alias_email = config['Sender']['sender_alias_email']
sender_name = config['Sender']['sender_name']

password = config['Sender']['password']

message_file = config["Message"]["filename"]
contacts_file = config["Contacts"]['filename']

with open(message_file) as f:
    message_html = f.read()
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)

        with open(contacts_file) as contact_list:
            contacts = csv.DictReader(contact_list, delimiter=',')
            for contact in contacts:

                message = MIMEMultipart()
                message["Subject"] = config["Message"]['subject'].format(**contact)
                message["From"] = "{sender_name} <{sender_alias_email}>".format(sender_name=sender_name, sender_alias_email=sender_alias_email)

                recipient_email = contact[config["Recipient"]["email_column"]]
                message["To"] = "{recipient_name} <{recipient_email}>".format(recipient_email=contact[config["Recipient"]["email_column"]], recipient_name=contact[config["Recipient"]["name_column"]])
                formatted_message_html = message_html.format(**contact)
                content = MIMEText(formatted_message_html, "html")
                message.attach(content)
                server.sendmail(
                    sender_alias_email, recipient_email, message.as_string()
                )