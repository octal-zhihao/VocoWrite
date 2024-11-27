#!/usr/bin/python3
# -*- coding:utf-8 -*-
from .fileupload import seve_file
import requests
import datetime
import hashlib
import base64
import hmac
import json
import os
import re
from pydub import AudioSegment

def convert_to_wav(input_file_path, output_file_path):
    """
    Convert audio file to .wav format.
    Args:
        input_file_path (str): The path of the input audio file (e.g., .mp3).
        output_file_path (str): The desired output file path for the .wav file.
    """
    # Load the audio file using pydub
    audio = AudioSegment.from_file(input_file_path)
    
    # Export as .wav
    audio.export(output_file_path, format="wav")
    print(f"File converted to {output_file_path}")

def merge_result_for_one_vad(result_vad):
    content = ""
    lst = 0
    for rt_dic in result_vad['st']['rt']:
        if result_vad['st']['rl'] != lst:
            # content += '\n'
            lst = result_vad['st']['rl']
        for st_dic in rt_dic['ws']:
            for cw_dic in st_dic['cw']:
                for w in cw_dic['w']:
                    content += w
    return content

path_pwd = os.path.split(os.path.realpath(__file__))[0]
os.chdir(path_pwd)


# 创建和查询
class get_result(object):
    def __init__(self, appid, apikey, apisecret, file_path, language="zh_cn"):
        # 以下为POST请求
        self.Host = "ost-api.xfyun.cn"
        self.RequestUriCreate = "/v2/ost/pro_create"
        self.RequestUriQuery = "/v2/ost/query"
        # 设置url
        if re.match("^\d", self.Host):
            self.urlCreate = "http://" + self.Host + self.RequestUriCreate
            self.urlQuery = "http://" + self.Host + self.RequestUriQuery
        else:
            self.urlCreate = "https://" + self.Host + self.RequestUriCreate
            self.urlQuery = "https://" + self.Host + self.RequestUriQuery
        self.HttpMethod = "POST"
        self.APPID = appid
        self.Algorithm = "hmac-sha256"
        self.HttpProto = "HTTP/1.1"
        self.UserName = apikey
        self.Secret = apisecret
        self.file_path = file_path

        # 设置当前时间
        cur_time_utc = datetime.datetime.utcnow()
        self.Date = self.httpdate(cur_time_utc)
        language_type = 1
        if language == "en":
            language_type = 3
        # 设置测试音频文件
        self.BusinessArgsCreate = {
            "language_type": language_type,
            "language": 'zh_cn',
            "accent": "mandarin",
            "domain": "pro_ost_ed",
            # "callback_url": "http://IP:端口号/xxx/"
        }

    def img_read(self, path):
        with open(path, 'rb') as fo:
            return fo.read()

    def hashlib_256(self, res):
        m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return result

    def httpdate(self, dt):
        """
        Return a string representation of a date according to RFC 1123
        (HTTP/1.1).
        The supplied date must be in UTC.
        """
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                        dt.year, dt.hour, dt.minute, dt.second)

    def generateSignature(self, digest, uri):
        signature_str = "host: " + self.Host + "\n"
        signature_str += "date: " + self.Date + "\n"
        signature_str += self.HttpMethod + " " + uri \
                         + " " + self.HttpProto + "\n"
        signature_str += "digest: " + digest
        signature = hmac.new(bytes(self.Secret.encode('utf-8')),
                             bytes(signature_str.encode('utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def init_header(self, data, uri):
        digest = self.hashlib_256(data)
        sign = self.generateSignature(digest, uri)
        auth_header = 'api_key="%s",algorithm="%s", ' \
                      'headers="host date request-line digest", ' \
                      'signature="%s"' \
                      % (self.UserName, self.Algorithm, sign)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": self.Host,
            "Date": self.Date,
            "Digest": digest,
            "Authorization": auth_header
        }
        return headers

    def get_create_body(self, fileurl):
        post_data = {
            "common": {"app_id": self.APPID},
            "business": self.BusinessArgsCreate,
            "data": {
                "audio_src": "http",
                "audio_url": fileurl,
                "encoding": "raw"
            }
        }
        body = json.dumps(post_data)
        return body

    def get_query_body(self, task_id):
        post_data = {
            "common": {"app_id": self.APPID},
            "business": {
                "task_id": task_id,
            },
        }
        body = json.dumps(post_data)
        return body

    def call(self, url, body, headers):

        try:
            response = requests.post(url, data=body, headers=headers, timeout=8)
            status_code = response.status_code
            interval = response.elapsed.total_seconds()
            if status_code != 200:
                info = response.content
                return info
            else:
                resp_data = json.loads(response.text)
                return resp_data
        except Exception as e:
            print("Exception ：%s" % e)

    def task_create(self):
        body = self.get_create_body(self.get_fileurl())
        headers_create = self.init_header(body, self.RequestUriCreate)
        task_id = self.call(self.urlCreate, body, headers_create)
        print(task_id)
        return task_id

    def task_query(self, task_id):
        if task_id:
            body = self.get_create_body(self.get_fileurl())
            query_body = self.get_query_body(task_id)
            headers_query = self.init_header(body, self.RequestUriQuery)
            result = self.call(self.urlQuery, query_body, headers_query)
            return result

    def get_fileurl(self):
        # 文件上传
        api = seve_file.SeveFile(app_id=self.APPID, api_key=self.UserName, api_secret=self.Secret, upload_file_path=self.file_path)
        file_total_size = os.path.getsize(self.file_path)
        if file_total_size < 31457280:
            fileurl = api.gene_params('/upload')['data']['url']
        else:
            fileurl = api.gene_params('/mpupload/upload')
        return fileurl
    
    def get_result(self):
        task_id = self.task_create()['data']['task_id']
        content = ""
        while True:
            result = self.task_query(task_id)
            if isinstance(result, dict) and result['data']['task_status'] != '1' and result['data'][
                'task_status'] != '2':
                print("转写完成···\n")
                js_xunfei_result = result['data']['result']
                for result_one_vad_str in js_xunfei_result['lattice']:
                    js_result_one_vad = result_one_vad_str['json_1best']
                    content += merge_result_for_one_vad(js_result_one_vad)
                break
            elif isinstance(result, bytes):
                print("发生错误···\n", result)
                break
        return content


def get_transcription(file_path, language):
    # 输入讯飞开放平台的appid，secret、key和文件路径
    appid = "93d8ec2d"
    apikey = "71f0d86d94f123f8c904b7b1b4fe0090"
    apisecret = "MjcyMmU0ODNmYjY1ZjFjZWNlM2UzOGU0"
    if not os.path.exists(file_path):
        print("文件不存在")
        return
    if not file_path.endswith(".wav"):
        convert_to_wav(file_path, file_path.replace(".wav", "_converted.wav"))
        file_path = file_path.replace(".wav", "_converted.wav")

    gClass = get_result(appid, apikey, apisecret, file_path, language)
    return gClass.get_result()

# if __name__ == '__main__':
#     print(get_transcription())