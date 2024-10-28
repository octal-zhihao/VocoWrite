# transcriber/urls.py
from django.urls import path
from .views import transcribe_audio

urlpatterns = [
    path('api/', transcribe_audio, name='transcribe_audio'),
]
