from opencc import OpenCC

# 创建 OpenCC 实例，设置为繁体转简体
cc = OpenCC('t2s')

def convert_traditional_to_simplified(traditional_text):
    """
    将繁体中文转换为简体中文
    :param traditional_text: 繁体中文文本
    :return: 转换后的简体中文文本
    """
    return cc.convert(traditional_text)
