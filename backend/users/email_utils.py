import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


GMAIL_ADDRESS = os.environ.get('GMAIL_ADDRESS', 'mobimama@gmail.com')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', '')


def send_otp_email(to_email, otp_code, first_name):
    """Send OTP verification email to nurse's student email."""
    if not GMAIL_APP_PASSWORD:
        print(f"[EMAIL SKIPPED] No GMAIL_APP_PASSWORD set. OTP for {to_email}: {otp_code}")
        return True

    subject = "Your Mobi Mama Verification Code"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; background-color: #f4f4f4; font-family: Arial, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 40px 0;">
            <tr>
                <td align="center">
                    <table width="500" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <tr>
                            <td style="background-color: #e91e63; padding: 30px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Mobi Mama</h1>
                                <p style="color: #ffffff; margin: 8px 0 0 0; font-size: 14px; opacity: 0.9;">Maternal Health Platform</p>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 40px 30px;">
                                <h2 style="color: #333333; margin: 0 0 20px 0; font-size: 20px;">Verify Your Email</h2>
                                <p style="color: #555555; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                                    Hi {first_name},
                                </p>
                                <p style="color: #555555; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                                    Thank you for registering as a nurse on Mobi Mama. Please use the verification code below to complete your registration:
                                </p>
                                <div style="background-color: #f8f9fa; border: 2px dashed #e91e63; border-radius: 8px; padding: 20px; text-align: center; margin: 0 0 30px 0;">
                                    <p style="color: #888888; font-size: 12px; margin: 0 0 10px 0; text-transform: uppercase; letter-spacing: 2px;">Your Verification Code</p>
                                    <p style="color: #e91e63; font-size: 36px; font-weight: bold; margin: 0; letter-spacing: 8px;">{otp_code}</p>
                                </div>
                                <p style="color: #e91e63; font-size: 14px; font-weight: bold; text-align: center; margin: 0 0 20px 0;">
                                    This code expires in 7 minutes.
                                </p>
                                <p style="color: #888888; font-size: 13px; line-height: 1.5; margin: 0;">
                                    If you did not request this verification, please ignore this email. Do not share this code with anyone.
                                </p>
                            </td>
                        </tr>
                        <tr>
                            <td style="background-color: #f8f9fa; padding: 20px 30px; text-align: center;">
                                <p style="color: #888888; font-size: 12px; margin: 0;">
                                    Mobi Mama - AI-Driven Maternal Health Platform
                                </p>
                                <p style="color: #888888; font-size: 12px; margin: 5px 0 0 0;">
                                    Built for rural and low-literacy communities in Africa
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"Mobi Mama <{GMAIL_ADDRESS}>"
    msg['To'] = to_email

    text_part = MIMEText(f"Your Mobi Mama verification code is: {otp_code}. It expires in 7 minutes.", 'plain')
    html_part = MIMEText(html_body, 'html')
    msg.attach(text_part)
    msg.attach(html_part)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())
        print(f"[EMAIL SENT] OTP to {to_email}")
        return True
    except Exception as e:
        print(f"[EMAIL WARN] 465 failed ({e}); trying 587 STARTTLS...")
        try:
            with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
                server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())
            print(f"[EMAIL SENT] OTP to {to_email} via 587")
            return True
        except Exception as e2:
            print(f"[EMAIL ERROR] Failed to send OTP to {to_email}: {e2}")
            return False
