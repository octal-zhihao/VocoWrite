from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from transformers import pipeline

# 创建全局模型实例
translator = pipeline("translation_en_to_zh", model="Helsinki-NLP/opus-mt-en-zh")

@method_decorator(csrf_exempt, name='dispatch')
class TranslationView(APIView):
    def post(self, request):
        texts = request.data.get("texts", [])  # 接收批量文本
        if not texts:
            return Response({"error": "No texts provided"}, status=400)
        
        # 批量翻译
        translations = translator(texts)
        translated_texts = [t['translation_text'] for t in translations]

        return Response({"translated_texts": translated_texts}, status=200)

