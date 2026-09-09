"""Gemini-powered OCR review of uploaded NMC licenses (PIN / AIN)."""

import json
import os
import re

import google.generativeai as genai

OCR_PROMPT = """
You are verifying a Ghana Nursing and Midwifery Council (NMC) practitioner license.
Look at the provided license document (photo or PDF) and return ONLY a JSON object with these keys:
{
  "full_name": "<full name exactly as printed>",
  "license_number": "<registration number / PIN / AIN exactly as printed>",
  "expiry_date": "<expiry date in YYYY-MM-DD, or null if not readable>",
  "is_valid": true or false,
  "notes": "<short note e.g. document is damaged / looks tampered / missing NMC logo>"
}
Rules:
- If this is clearly not an NMC/Ghana license document, set is_valid to false and explain in notes.
- If key text (name, number, expiry) is unreadable, set is_valid to false and note what is missing.
Do not output anything except the JSON object.
"""


def _extract_json(text):
    cleaned = (text or "").strip()
    cleaned = re.sub(r'```(?:json)?\s*', '', cleaned).strip('`')
    match = re.search(r'\{.*\}', cleaned, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def _guess_mime(filename):
    ext = (filename or '').lower().rsplit('.', 1)[-1]
    return {
        'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png',
        'webp': 'image/webp', 'heic': 'image/heic', 'pdf': 'application/pdf',
    }.get(ext, 'image/jpeg')


def verify_license_content(content: bytes, filename: str) -> dict:
    """Ask Gemini to extract licence details from uploaded bytes.

    Returns: {"success": bool, "data": dict, "error": str}
    """
    api_key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not api_key or api_key.lower().startswith('your-'):
        return {'success': False, 'data': {}, 'error': 'GEMINI_API_KEY not configured'}

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        image_part = {'mime_type': _guess_mime(filename), 'data': content}
        response = model.generate_content([OCR_PROMPT, image_part])
        parsed = _extract_json(response.text)
        if not parsed:
            return {'success': False, 'data': {}, 'error': 'OCR returned no parseable JSON'}
        return {'success': True, 'data': parsed, 'error': ''}
    except Exception as exc:  # noqa: BLE001
        return {'success': False, 'data': {}, 'error': str(exc)}