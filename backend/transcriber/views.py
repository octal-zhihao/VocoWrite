# transcriber/views.py
from django.http import JsonResponse
# from transformers import MarianMTModel, MarianTokenizer
from rest_framework.decorators import api_view
from rest_framework import status
import tempfile
import whisper
import os

# 加载 Whisper 模型
model = whisper.load_model("base")

# 加载 Marian 模型用于翻译（英文转中文）
# translator_model_name = "Helsinki-NLP/opus-mt-en-zh"
# translator_model = MarianMTModel.from_pretrained(translator_model_name)
# translator_tokenizer = MarianTokenizer.from_pretrained(translator_model_name)

# def translate_text(text):
#     # 将文本翻译成中文
#     tokens = translator_tokenizer([text], return_tensors="pt", truncation=True, padding="max_length", max_length=512)
#     translation = translator_model.generate(**tokens)
#     translated_text = translator_tokenizer.decode(translation[0], skip_special_tokens=True)
#     return translated_text

@api_view(['POST'])
def transcribe_audio(request):
    if 'audio' not in request.FILES:
        return JsonResponse({"error": "没有上传文件"}, status=status.HTTP_400_BAD_REQUEST)
    
    if 'language' not in request.data:
        return JsonResponse({"error": "没有指定语言"}, status=status.HTTP_400_BAD_REQUEST)

    audio_file = request.FILES['audio']
    language = request.data['language']  # 获取语言参数
    
    # 使用临时文件保存上传的音频文件
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        for chunk in audio_file.chunks():
            temp_file.write(chunk)
        temp_file_path = temp_file.name  # 获取临时文件的路径

    try:
        # 设置任务类型和语言
        if language == "chinese":
            # 中文音频，直接转录为中文
            result = model.transcribe(temp_file_path, task='transcribe', language='zh')
            transcription = result['text']
        else:
            # 英文音频，转录并翻译为中文
            result = model.transcribe(temp_file_path, task='translate', language='en')
            transcription = result['text']
            # 使用 Marian 模型将英文转录结果翻译为中文
            # translated = translate_text(transcription)
            # transcription = translated  # 更新为翻译后的中文文本
        

        # 可选择在转录完成后删除临时文件
        os.remove(temp_file_path)

        return JsonResponse({"transcription": transcription})
    except Exception as e:
        print(f"转录过程中的错误: {e}")

        # 在错误发生时，确保删除临时文件
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        return JsonResponse({"error": "转录失败"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
