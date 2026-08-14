from django.urls import path
from .views import chat_with_mobi, voice_chat

urlpatterns = [
   path("", chat_with_mobi, name="chat_with_mobi"),
    path("voice/", voice_chat, name="voice_chat"),
]