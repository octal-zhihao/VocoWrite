import os
import logging
import tempfile
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from pydub import AudioSegment
import time
from .utils import get_transcription
# 配置日志记录
logger = logging.getLogger(__name__)


@api_view(['POST'])
def transcribe_audio(request):
    if 'audio' not in request.FILES:
        return JsonResponse({"error": "没有上传文件"}, status=status.HTTP_400_BAD_REQUEST)
    
    if 'language' not in request.data:
        return JsonResponse({"error": "没有指定语言"}, status=status.HTTP_400_BAD_REQUEST)

    audio_file = request.FILES['audio']
    language = request.data['language']
    
    # 使用临时文件保存上传的音频文件
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav_file:
        try:
            # 检测音频格式并转换为 WAV
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in audio_file.chunks():
                    temp_file.write(chunk)
                
                temp_file_path = temp_file.name

                # 将音频文件转换为 WAV 格式
                audio = AudioSegment.from_file(temp_file_path)
                audio.export(temp_wav_file.name, format="wav")
                
            temp_wav_file_path = temp_wav_file.name
            # 根据语言选择句子分割符
            if language == "english":
                transcription = get_transcription(temp_wav_file_path, 'en')
                sentences = transcription.split('.')
            else:  # 默认是中文
                transcription = get_transcription(temp_wav_file_path, 'zh_cn')
                sentences = transcription.split('。')
            formatted_result = []
            for sentence in sentences:
                if sentence:  # 确保句子不为空
                    formatted_result.append(sentence.strip() + ('。' if language == "chinese" else '.'))


            # 将格式化结果作为响应返回
            return Response({'transcription': "\n".join(formatted_result)})

        except Exception as e:
            print(f"转录过程中的错误: {e}")
            return JsonResponse({"error": "转录失败"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        finally:
            # 清理临时文件
            try:
                time.sleep(1)
                os.remove(temp_wav_file_path)
            except PermissionError:
                print(f"无法删除文件 {temp_wav_file_path}，文件可能正在被使用。")
        