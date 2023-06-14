import os
import tkinter as tk
import re
from bs4 import BeautifulSoup
import cssutils
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

def colorize(event):
    # Define patterns for tags and attributes
    patterns = [
        ("<[./a-zA-Z]+>", "red"),  # HTML tags
        ('"[a-zA-Z0-9:;.,_# -]+"', "blue"),  # HTML attribute values
    ]

    for pattern, tag in patterns:
        body_text.tag_remove(tag, '1.0', tk.END)  # Remove previous tags

    # Apply each pattern
    for pattern, tag in patterns:
        start = 1.0
        while True:
            pos = body_text.search(pattern, start, stopindex=tk.END, regexp=True)
            if not pos:
                break
            end = f"{pos}+{len(body_text.get(pos))}c"
            body_text.tag_add(tag, pos, end)
            start = end
        body_text.tag_config(tag, foreground=tag)  # Set tag color


def fetch_css(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response
    return response.text


def style_to_inline():
    html = body_text.get('1.0', tk.END)
    soup = BeautifulSoup(html, 'html.parser')

    # Convert <style> tags
    styles = soup.findAll('style')
    for style in styles:
        css = cssutils.parseString(style.encode_contents())
        for rule in css:
            if rule.type == rule.STYLE_RULE:
                selector = rule.selectorText
                styles = rule.style.cssText
                # Find tags that match this selector
                tags = soup.select(selector)
                for tag in tags:
                    # Add inline style to tags
                    if 'style' in tag.attrs:
                        tag['style'] += f'; {styles}'
                    else:
                        tag['style'] = styles

        # Remove the <style> tag
        style.decompose()
    # Convert <link rel="stylesheet"> tags
    links = soup.findAll('link', rel='stylesheet')
    for link in links:
        url = link['href']
        css = fetch_css(url)
        css = cssutils.parseString(css)
        for rule in css:
            if rule.type == rule.STYLE_RULE:
                selector = rule.selectorText
                styles = rule.style.cssText
                # Find tags that match this selector
                tags = soup.select(selector)
                for tag in tags:
                    # Add inline style to tags
                    if 'style' in tag.attrs:
                        tag['style'] += f'; {styles}'
                    else:
                        tag['style'] = styles

        # Remove the <link> tag
        link.decompose()

    # Update the textbox with the new HTML
    body_text.delete('1.0', tk.END)
    body_text.insert('1.0', str(soup))

    email = email_entry.get()
    recipient = recipient_entry.get()
    body = body_text.get('1.0', tk.END)
    password = password_entry.get()
    subject = subject_entry.get()

    emailsender(recipient,subject,body,email,password)

def save_email():
    email = email_entry.get()

    password = password_entry.get()
    with open('email_credentials.txt', 'w') as file:
        file.write(f"Email: {email}\n")
        file.write(f"Password: {password}\n")

        # Clear the input fields


    # Perform the necessary actions to save the email information
    # You can implement your logic here

    print("Email Saved!")


def logout():
    # Perform the necessary actions to log out
    # You can implement your logic here
    os.remove("email_credentials.txt")
    if os.path.exists("email_credentials.txt"):
        os.remove("email_credentials.txt")
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    print("Logged out!")

def emailsender(to, subject, body,form,password):
    # Set up the message headers
    msg = MIMEMultipart()
    msg['To'] =formataddr(('Recipient', ', '.join(to)))
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(form, password)
        smtp.sendmail(form, to, msg.as_string())


# Check if the user and password file exists

root = tk.Tk()
root.configure(bg='#F0F0F0')  # Set background color

header_label = tk.Label(root, text="Email Sender App", font=("Arial", 24, "bold"), bg='#333', fg='white', pady=10)
header_label.pack(fill=tk.X)

frame = tk.Frame(root, bg='#F0F0F0')
frame.pack(pady=20)

email_label = tk.Label(frame, text="Email:", font=("Arial", 14), bg='#F0F0F0')
email_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
email_entry = tk.Entry(frame, font=("Arial", 14))
email_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

password_label = tk.Label(frame, text="Password:", font=("Arial", 14), bg='#F0F0F0')
password_label.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)
password_entry = tk.Entry(frame, show="*", font=("Arial", 14))
password_entry.grid(row=0, column=3, padx=10, pady=5, sticky=tk.W)


recipient_label = tk.Label(frame, text="Recipient:", font=("Arial", 14), bg='#F0F0F0')
recipient_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
recipient_entry = tk.Entry(frame, font=("Arial", 14))
recipient_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)


subject_label = tk.Label(frame, text="Subject:", font=("Arial", 14), bg='#F0F0F0')
subject_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
subject_entry = tk.Entry(frame, font=("Arial", 14))
subject_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

body_label = tk.Label(frame, text="Body:", font=("Arial", 14), bg='#F0F0F0')
body_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
body_text = tk.Text(frame, font=("Arial", 14), height=10, width=40)
body_text.grid(row=4, column=1, columnspan=3, padx=10, pady=5, sticky=tk.W)

button_frame = tk.Frame(root, bg='#F0F0F0')
button_frame.pack(pady=10)

save_button = tk.Button(button_frame, text="Save Email and password", font=("Arial", 14), command=save_email)
save_button.pack(side=tk.LEFT, padx=10)
save_button = tk.Button(button_frame, text="send Email", font=("Arial", 14), command=style_to_inline)
save_button.pack(side=tk.LEFT, padx=10)

logout_button = tk.Button(button_frame, text="Logout", font=("Arial", 14), command=logout)
logout_button.pack(side=tk.LEFT, padx=10)
if os.path.exists('email_credentials.txt'):
    # Read the email and password from the file
    with open('email_credentials.txt', 'r') as file:
        lines = file.readlines()
        if len(lines) >= 2:
            email = lines[0].strip().split(': ')[1]
            password = lines[1].strip().split(': ')[1]

            # Fill the email and password fields
            email_entry.insert(tk.END, email)
            password_entry.insert(tk.END, password)
root.mainloop()
