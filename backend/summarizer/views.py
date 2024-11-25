from rest_framework.response import Response
from rest_framework.decorators import api_view
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 初始化模型和tokenizer（全局加载避免重复）
tokenizer = AutoTokenizer.from_pretrained("D:\\CodeField\\VocoWrite\\backend\\summarizer\\mT5_multilingual_XLSum", legacy=False)
model = AutoModelForSeq2SeqLM.from_pretrained("D:\\CodeField\\VocoWrite\\backend\\summarizer\\mT5_multilingual_XLSum")

@api_view(['POST'])
def summarize_text(request):
    text = request.data.get("text", "")
    if not text:
        return Response({"error": "Text is required"}, status=400)
    text = "这是一段会议实录文本: " + text
    # 生成摘要
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return Response({"summary": summary}, status=200)
