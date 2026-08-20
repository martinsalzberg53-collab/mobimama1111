import os
import logging

logger = logging.getLogger(__name__)

_at_client = None


def _get_client():
    global _at_client
    if _at_client is None:
        api_key = os.environ.get("AT_API_KEY")
        username = os.environ.get("AT_USERNAME", "sandbox")
        if not api_key:
            logger.warning("AT_API_KEY not set — SMS disabled")
            return None
        import africastalking
        africastalking.initialize(username=username, api_key=api_key)
        _at_client = africastalking.SMS
    return _at_client


def send_sms(to_number: str, message: str) -> bool:
    """Send an SMS via Africa's Talking. Returns True on success."""
    client = _get_client()
    if not client:
        logger.info(f"SMS skipped (no API key): {message[:60]}")
        return False
    try:
        sender_id = os.environ.get("AT_SENDER_ID", "MobiMama")
        result = client.send(message, [to_number], sender_id=sender_id)
        recipients = result.get("SMSMessageData", {}).get("Recipients", [])
        for r in recipients:
            if r.get("statusCode") in (100, 101):
                return True
        logger.warning(f"SMS delivery uncertain: {result}")
        return False
    except Exception as e:
        logger.error(f"SMS failed: {e}")
        return False


def send_appointment_confirmation(phone: str, clinic_name: str, date_time: str) -> bool:
    msg = (
        f"Mobi Mama: Your appointment at {clinic_name} "
        f"on {date_time} has been booked successfully. "
        f"You will be notified when a nurse reviews it."
    )
    return send_sms(phone, msg)


def send_appointment_approved(phone: str, clinic_name: str) -> bool:
    msg = (
        f"Mobi Mama: Your appointment at {clinic_name} has been approved. "
        f"Please visit the hospital as scheduled. Stay safe!"
    )
    return send_sms(phone, msg)


def send_appointment_cancelled(phone: str) -> bool:
    msg = (
        "Mobi Mama: Your appointment has been cancelled. "
        "Please book a new one if you still need care."
    )
    return send_sms(phone, msg)


def send_reminder(phone: str, clinic_name: str, date_time: str) -> bool:
    msg = (
        f"Mobi Mama reminder: You have an appointment at {clinic_name} "
        f"tomorrow ({date_time}). Please prepare accordingly."
    )
    return send_sms(phone, msg)
