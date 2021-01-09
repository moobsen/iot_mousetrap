import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
def send_mail(smtp_user, pw, mail, receiver_email):
    try:
        port = 465  # For SSL
        sender_email = smtp_user

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("mail.bluebirdmountain.de", port, context=context) as server:
            server.login(sender_email, pw)
            server.sendmail(sender_email, receiver_email, mail)
    except Exception as ex:
        print(ex)

def load_config():
    try:
        env_vars = {}
        with open("/home/pi/src/mousetrap/.env") as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                key, value = line.strip().split('=', 1)
                env_vars.update({key: value}) # Save to a dict
        return env_vars
    except  Exception as ex:
        print(ex)

def main(): 
    config = load_config()
    sender_email = config['SMTP_USER']
    receiver_email = config['MAIL_RECEIVER']
    password = config['SMTP_PW']

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your mouse trap has closed"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = 'You probably want to check if you have caught something...'
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    send_mail(sender_email, password, message.as_string(), receiver_email)

if __name__ == "__main__":
    main()
