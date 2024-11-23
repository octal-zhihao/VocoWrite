from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from transformers import pipeline

class TranslationView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.translator = pipeline("translation_en_to_zh", model="Helsinki-NLP/opus-mt-en-zh")

    def post(self, request):
        text = request.data.get("text", "")
        if not text:
            return Response({"error": "No text provided"}, status=400)

        translation = self.translator(text)
        translated_text = translation[0]["translation_text"]

        return Response({"translated_text": translated_text}, status=200)
