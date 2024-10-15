import re

def extract_number_from_string(s):
    # 使用正则表达式匹配字符串中的数字
    match = re.search(r'\d+', s)
    if match:
        # 将匹配到的字符串数字转换为整数
        number = int(match.group())
        return number
    else:
        # 如果没有匹配到数字，返回 None 或者其他默认值
        return None

# 测试
string = "2 分钟前"
number = extract_number_from_string(string)
print(number)  # 输出: 2