import smtplib
from email.message import EmailMessage

from config import RECIPIENT_EMAIL, SENDER_EMAIL, SENDER_PASSWORD


def send_alert(product_title: str, product_url: str, current_price: float, target_price: float):
    """Sends an email alert for a price drop."""
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL]):
        print("Email credentials not set. Skipping email alert.")
        print("Please set SENDER_EMAIL, SENDER_PASSWORD, and RECIPIENT_EMAIL in your .env file.")
        return

    subject = f"Price Alert: {product_title}"
    body = f"""
    Great news!

    The price for '{product_title}' has dropped below your target of ${target_price:.2f}.

    The current price is now ${current_price:.2f}.

    You can buy it here: {product_url}

    Happy shopping!
    """

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL

    try:
        print("Connecting to email server...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("Sending email alert...")
            smtp.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
