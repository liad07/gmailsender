import os
from flask import Flask, render_template, request
import re
from bs4 import BeautifulSoup
import cssutils
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

app = Flask(__name__)
html_code = '''<!DOCTYPE html>
<html>
<head>
    <title>Email Sender App</title>
</head>
<body>
    <h1>Email Sender App</h1>
    <form method="POST" action="/">
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br><br>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>

        <label for="recipient">Recipient:</label>
        <input type="email" id="recipient" name="recipient" required><br><br>

        <label for="subject">Subject:</label>
        <input type="text" id="subject" name="subject" required><br><br>

        <label for="body">Body:</label><br>
        <textarea id="body" name="body" rows="10" cols="50" required></textarea><br><br>

        <input type="submit" value="Send Email">
    </form>
</body>
</html>'''
@app.route('/', methods=['GET', 'POST'])
def email_sender():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        recipient = request.form['recipient']
        subject = request.form['subject']
        body = request.form['body']

        emailsender(recipient, subject, body, email, password)

        return "Email Sent!"
    return html_code

def emailsender(to, subject, body, form, password):
    # Set up the message headers
    msg = MIMEMultipart()
    msg['To'] = formataddr(('Recipient', ', '.join(to)))
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(form, password)
        smtp.sendmail(form, to, msg.as_string())

if __name__ == '__main__':
    app.run(debug=True)
