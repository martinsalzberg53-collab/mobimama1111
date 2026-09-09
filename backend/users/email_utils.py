import json
import os
import urllib.request


GMAIL_ADDRESS = os.environ.get('GMAIL_ADDRESS', 'mobimamagh@gmail.com')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', '')

RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')
RESEND_FROM = os.environ.get('RESEND_FROM', 'Mobi Mama <onboarding@resend.dev>')

BREVO_API_KEY = os.environ.get('BREVO_API_KEY', '')
BREVO_SENDER_EMAIL = os.environ.get('BREVO_SENDER_EMAIL', GMAIL_ADDRESS)
BREVO_SENDER_NAME = os.environ.get('BREVO_SENDER_NAME', 'Mobi Mama')

EMAILJS_PUBLIC_KEY = os.environ.get('EMAILJS_PUBLIC_KEY', '')
EMAILJS_PRIVATE_KEY = os.environ.get('EMAILJS_PRIVATE_KEY', '')
EMAILJS_SERVICE_ID = os.environ.get('EMAILJS_SERVICE_ID', '')
EMAILJS_TEMPLATE_ID = os.environ.get('EMAILJS_TEMPLATE_ID', '')


def _html_body(first_name, otp_code):
    return f"""
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


def _text_body(first_name, otp_code):
    return (f"Hi {first_name},\n\nThank you for registering as a nurse on Mobi Mama. "
            f"Your verification code is: {otp_code}. It expires in 7 minutes.\n\n"
            "If you did not request this, please ignore this email.")


def _send_via_emailjs(to_email, first_name, otp_code):
    """EmailJS REST API — sends FROM the connected Gmail (mobimamagh) via HTTPS."""
    payload = {
        "service_id": EMAILJS_SERVICE_ID,
        "template_id": EMAILJS_TEMPLATE_ID,
        "user_id": EMAILJS_PUBLIC_KEY,
        "template_params": {
            "to_email": to_email,
            "email": to_email,
            "first_name": first_name or "there",
            "otp_code": otp_code,
        },
    }
    if EMAILJS_PRIVATE_KEY:
        payload["accessToken"] = EMAILJS_PRIVATE_KEY
    req = urllib.request.Request(
        "https://api.emailjs.com/api/v1.0/email/send",
        data=json.dumps(payload).encode('utf-8'),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://mobi-mama.onrender.com",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = resp.read().decode('utf-8', 'replace')
        print(f"[EMAIL SENT] EmailJS OTP to {to_email}: HTTP {resp.status} {body[:200]}")
        return True


def _send_via_resend(to_email, first_name, otp_code):
    """Try Resend's HTTP API first (works on Render; uses port 443 only)."""
    payload = json.dumps({
        "from": RESEND_FROM,
        "to": [to_email],
        "subject": "Your Mobi Mama Verification Code",
        "html": _html_body(first_name, otp_code),
        "text": _text_body(first_name, otp_code),
    }).encode('utf-8')
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = resp.read().decode('utf-8', 'replace')
        print(f"[EMAIL SENT] Resend OTP to {to_email}: HTTP {resp.status} {body[:200]}")
        return True


def _send_via_brevo(to_email, first_name, otp_code):
    """Brevo HTTP API (free tier, no domain needed, works on Render via port 443)."""
    payload = json.dumps({
        "sender": {
            "email": BREVO_SENDER_EMAIL,
            "name": BREVO_SENDER_NAME,
        },
        "to": [{"email": to_email}],
        "subject": "Your Mobi Mama Verification Code",
        "htmlContent": _html_body(first_name, otp_code),
        "textContent": _text_body(first_name, otp_code),
    }).encode('utf-8')
    req = urllib.request.Request(
        "https://api.brevo.com/v3/smtp/email",
        data=payload,
        method="POST",
        headers={
            "api-key": BREVO_API_KEY,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = resp.read().decode('utf-8', 'replace')
        print(f"[EMAIL SENT] Brevo OTP to {to_email}: HTTP {resp.status} {body[:200]}")
        return True


def _send_via_gmail_smtp(to_email, otp_code):
    """Fallback: Gmail SMTP (often blocked on Render free tier)."""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Your Mobi Mama Verification Code"
    msg['From'] = f"Mobi Mama <{GMAIL_ADDRESS}>"
    msg['To'] = to_email
    msg.attach(MIMEText(otp_code, 'plain'))
    msg.attach(MIMEText(f"Your Mobi Mama verification code is: {otp_code}. It expires in 7 minutes.", 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())
        print(f"[EMAIL SENT] OTP to {to_email} via Gmail 465")
        return True
    except Exception as e:
        print(f"[EMAIL WARN] Gmail 465 failed ({e}); trying 587 STARTTLS...")
        try:
            with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
                server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())
            print(f"[EMAIL SENT] OTP to {to_email} via Gmail 587")
            return True
        except Exception as e2:
            print(f"[EMAIL ERROR] Gmail SMTP failed for {to_email}: {e2}")
            return False


def send_otp_email(to_email, otp_code, first_name):
    """Send OTP: EmailJS (from user's Gmail) -> Brevo -> Resend -> Gmail SMTP -> logs."""
    if EMAILJS_PUBLIC_KEY and EMAILJS_SERVICE_ID and EMAILJS_TEMPLATE_ID:
        try:
            return _send_via_emailjs(to_email, first_name, otp_code)
        except Exception as e:
            print(f"[EMAIL WARN] EmailJS failed for {to_email}: {e}")

    if BREVO_API_KEY:
        try:
            return _send_via_brevo(to_email, first_name, otp_code)
        except Exception as e:
            print(f"[EMAIL WARN] Brevo failed for {to_email}: {e}")

    if RESEND_API_KEY:
        try:
            return _send_via_resend(to_email, first_name, otp_code)
        except Exception as e:
            print(f"[EMAIL WARN] Resend failed for {to_email}: {e}")

    if GMAIL_APP_PASSWORD:
        return _send_via_gmail_smtp(to_email, otp_code)

    print(f"[EMAIL SKIPPED] No email provider configured. OTP for {to_email}: {otp_code}")
    return True