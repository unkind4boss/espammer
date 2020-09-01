# -*- coding: utf-8 -*-
import email, smtplib, ssl
import getpass
import csv

from time import sleep

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "your@gmail.com"
password = getpass.getpass("Type your password and press enter:")

with open("contacts_file.csv") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for corp_name,email,file_type,name in reader:
        print(f"Sending email to {corp_name}, {name}")
        # Send email here

        subject = "spammer"
        body = f"Hi, {name}, the email was sander with python"
        receiver_email = f"{email}"

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = f"{file_type}"  # In same directory as script

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(
                sender_email, password
            )
            server.sendmail(
                sender_email,
                receiver_email,
                text
            )
        print("sleep 10 min")
        sleep(60*10)
