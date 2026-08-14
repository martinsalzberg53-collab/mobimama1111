import os
import tempfile

from rest_framework.decorators import (
    api_view,
    permission_classes,
    parser_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


# ---------------- GEMINI CONFIG ----------------

_gemini_model = None
whisper_model = None


def get_gemini_model():
    global _gemini_model
    if _gemini_model is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is not set. "
                "Add it in the Render dashboard (Service > Environment)."
            )
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        _gemini_model = genai.GenerativeModel("gemini-2.5-flash")
    return _gemini_model


def get_whisper_model():
    global whisper_model
    if whisper_model is None:
        import whisper

        whisper_model = whisper.load_model("base")
    return whisper_model


# ---------------- TEXT CHAT ----------------

@api_view(["POST"])
@permission_classes([AllowAny])
def chat_with_mobi(request):
    try:
        message = request.data.get("message", "").strip()

        if not message:
            return Response(
                {"error": "Message is required"},
                status=400,
            )

        prompt = f"""
You are Mobi AI, a trusted maternal health assistant for Ghana.

You can speak:
- English
- Twi (Akan)

Rules:
- Always reply in the SAME language as the user.
- If the user asks you to speak Twi, reply completely in Twi.
- If the user writes in Twi, reply in Twi.
- If the user writes in English, reply in English.
- Use simple, friendly language.
- Never diagnose diseases.
- Never prescribe dangerous medication.
- Encourage users with emergency symptoms to visit the nearest hospital immediately.
- Keep responses short and easy to understand.

User:
{message}
"""

        response = get_gemini_model().generate_content(prompt)

        return Response({
            "reply": response.text
        })

    except Exception as e:
        return Response({
            "error": str(e)
        }, status=500)


# ---------------- VOICE CHAT ----------------

@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def voice_chat(request):

    audio_file = request.FILES.get("audio")

    if not audio_file:
        return Response(
            {"error": "No audio file received"},
            status=400,
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        for chunk in audio_file.chunks():
            tmp.write(chunk)

        tmp_path = tmp.name

    try:
        # Convert speech to text
        speech_model = get_whisper_model()
        result = speech_model.transcribe(tmp_path)

        user_text = result["text"]

        prompt = f"""
You are Mobi AI, a trusted maternal health assistant for Ghana.

You can speak:
- English
- Twi (Akan)

Rules:
- Reply in the SAME language used by the user.
- If the user speaks Twi, answer in Twi.
- If the user speaks English, answer in English.
- Be simple and helpful.
- Never diagnose diseases.
- Encourage hospital visits for emergencies.

User:
{user_text}
"""

        ai_response = get_gemini_model().generate_content(prompt)

        return Response({
            "transcribed_text": user_text,
            "reply": ai_response.text,
        })

    except Exception as e:
        return Response({
            "error": str(e)
        }, status=500)

    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass