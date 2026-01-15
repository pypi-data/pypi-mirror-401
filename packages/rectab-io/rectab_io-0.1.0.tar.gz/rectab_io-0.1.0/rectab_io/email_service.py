import smtplib
from email.mime.text import MIMEText

# Your Gmail credentials (hardcoded as requested)
SENDER_EMAIL = "louatimahdi390@gmail.com"
APP_PASSWORD = "nucm mizw szlu oloq"

def send_access_token_email(user_email: str, user_fullname: str, access_token: str):
    """Send welcome email with access token to the user"""
    subject = "Welcome to Rectab.io - Your Access Token"
    
    body = f"""
    Hello {user_fullname},

    Thank you for using Rectab.io Recommendation Systems Analytics Library! 🎉

    Your unique access token is:
    {access_token}

    This token has been automatically saved to your system configuration. You can now start using the library without manually entering the token.

    If you need any help, feel free to reach out.

    Best Regards,
    Louati Mahdi
    Rectab.io
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = user_email

    try:
        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False