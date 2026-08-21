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

LANGUAGE_MAP = {
    "en": "English",
    "tw": "Twi (Akan)",
    "ga": "Ga",
    "ew": "Ewe",
    "ha": "Hausa",
}


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


def _build_prompt(message: str, language: str = "en") -> str:
    lang_name = LANGUAGE_MAP.get(language, "English")
    return f"""
You are Mobi AI, a trusted maternal health assistant for Ghana.

You can speak: English, Twi (Akan), Ga, Ewe, and Hausa.

Rules:
- ALWAYS reply in {lang_name}, regardless of what language the user writes in.
- Use simple, friendly language.
- Never diagnose diseases.
- Never prescribe dangerous medication.
- Encourage users with emergency symptoms to visit the nearest hospital immediately.
- Keep responses short and easy to understand.

User:
{message}
"""


# ---------------- TEXT CHAT ----------------

@api_view(["POST"])
@permission_classes([AllowAny])
def chat_with_mobi(request):
    try:
        message = request.data.get("message", "").strip()
        language = request.data.get("language", "en")

        if not message:
            return Response(
                {"error": "Message is required"},
                status=400,
            )

        prompt = _build_prompt(message, language)
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
    language = request.data.get("language", "en")

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
        speech_model = get_whisper_model()
        result = speech_model.transcribe(tmp_path)

        user_text = result["text"]

        prompt = _build_prompt(user_text, language)
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
