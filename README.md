# Gmail Sender App

This is a simple email sender application built using Tkinter, a GUI toolkit for Python, that allows you to send emails with HTML content. The application provides a user-friendly interface where you can enter the email sender's credentials, recipient, subject, and body of the email. It also supports saving the email credentials and logging out.

## Prerequisites

To run this application, you need to have the following prerequisites:

- Python 3.x installed on your system
- `tkinter` library installed (usually included in Python standard library)
- `beautifulsoup4` library installed (can be installed using `pip install beautifulsoup4`)
- `cssutils` library installed (can be installed using `pip install cssutils`)
- `requests` library installed (can be installed using `pip install requests`)
- `smtplib` library installed (usually included in Python standard library)

## Usage

1. Clone the repository or download the source code files.

2. Open a terminal or command prompt and navigate to the directory where the files are located.

3. Run the following command to start the application:

   ```bash
   python email_sender_app.py
   ```

4. The Email Sender App window will open.

5. Enter the email address and password of the email sender in the respective fields.

6. Enter the recipient's email address in the "Recipient" field.

7. Enter the subject of the email in the "Subject" field.

8. Enter the body of the email in the "Body" text area. You can use HTML tags and inline CSS to format the content.

9. Click the "Save Email and password" button to save the email credentials (optional).

10. Click the "Send Email" button to send the email. The HTML content will be processed to convert any external CSS into inline styles before sending.

11. To log out, click the "Logout" button. This will remove the saved email credentials (if any) and clear the input fields.

**Note:** If there is an existing `email_credentials.txt` file in the same directory as the application, the email and password fields will be automatically filled with the saved credentials when the application starts.

## Additional Information

- The application uses the `tkinter` library to create the graphical user interface.

- The `beautifulsoup4` library is used to parse the HTML content and convert external CSS into inline styles.

- The `cssutils` library is used to parse and manipulate CSS styles.

- The `requests` library is used to fetch external CSS files.

- The `smtplib` library is used to connect to the SMTP server and send the email.

- The email is sent using the Gmail SMTP server. If you want to use a different email provider, you need to modify the SMTP server details in the `emailsender()` function.

- The email credentials are saved in a text file named `email_credentials.txt` in the same directory as the application. The file format is as follows:

  ```
  Email: [email_address]
  Password: [password]
  ```

- The `save_email()` function is responsible for saving the email credentials to the file.

- The `logout()` function deletes the `email_credentials.txt` file and clears the input fields.

- The `style_to_inline()` function converts any external CSS styles in the HTML content to inline styles before sending the email.

- The application provides basic error handling and validation. However, it is recommended to perform additional testing and validation as per your specific requirements.

- The application's GUI elements are styled with default Tkinter styling. You can customize the styling further if desired.

Feel free to modify and enhance the application as needed to suit your requirements.
