# coding: utf-8
import SparkApi
import time
import os

# 以下密钥信息从控制台获取 https://console.xfyun.cn/services/bm35
appid = "d62e3ac9"  # 填写控制台中获取的 APPID 信息
api_secret = "NjdjZTMxYjZiYWYwZjZiZjRhOGFiYzUx"  # 填写控制台中获取的 APISecret 信息
api_key = "4fd5330f81172e16eb3a15bc63cb911e"  # 填写控制台中获取的 APIKey 信息

domain = "max-32k"      # Max版本
# domain = "pro-128k"  # Pro版本
# domain = "general"         # Lite版本

Spark_url = "wss://spark-api.xf-yun.com/chat/max-32k"   # Max服务地址
# Spark_url = "wss://spark-api.xf-yun.com/chat/pro-128k"  # Pro服务地址
# Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"  # Lite服务地址

# 初始上下文内容，当前可传system、user、assistant 等角色
text = [
    {"role": "system",
     "content": "假定你现在是一名记者，你的任务是把用户的每一次输入的文本进行总结凝练概括，要求输出的文字数量大约为20个字左右"}
]
text1 = {"role": "system",
     "content": "假定你现在是一名记者，你的任务是把用户的每一次输入的文本进行总结凝练概括，要求输出的文字数量大约为20个字左右"}

def getText(role, content):
    jsoncon = {"role": role, "content": content}
    text.append(jsoncon)
    return text


def getlength(text):
    length = sum(len(content["content"]) for content in text)
    return length


def checklen(text):
    while getlength(text) > 8000:
        del text[0]
    return text


def split_text(text, chunk_size=5000):
    """按指定大小分割文本"""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def get_output_filename(base_dir="./output", base_name="output"):
    """获取一个可用的输出文件名，按序号递增"""
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)  # 创建output目录
    count = 1
    while os.path.exists(os.path.join(base_dir, f"{base_name}{count}.txt")):
        count += 1
    return os.path.join(base_dir, f"{base_name}{count}.txt")


if __name__ == '__main__':
    try:
        # 确定输出文件名
        output_filename = get_output_filename()

        # 读取整个文件内容为一个字符串，并去掉所有换行符
        with open("input/input.txt", "r", encoding="utf-8") as file:
            full_text = file.read().replace("\n", "").strip()  # 去掉换行符和两端空白

        # 将文本按5000字分割
        text_chunks = split_text(full_text, 5000)

        for chunk in text_chunks:
            question = checklen(getText("user", chunk))
            SparkApi.answer = ""
            print("星火:", end="")
            SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)

            # 仅将 Spark API 的响应内容写入输出文件
            with open(output_filename, "a", encoding="utf-8") as outfile:
                outfile.write(f"星火: {SparkApi.answer}\n\n")

            # 删除最后一项（即最新的回答）以控制上下文长度
            text.pop()

            # 设置延时，避免频繁请求
            time.sleep(2)

        # 清空输入文件内容（避免重复读取）
        # with open("input/input.txt", "w", encoding="utf-8") as file:
        #     file.write("")

    except Exception as e:
        print(f"错误: {e}")
