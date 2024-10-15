import re

def extract_number_from_string(s):
    # 使用正则表达式匹配字符串中的数字，包括小数
    match = re.search(r'\d+(\.\d+)?', s)
    if match:
        # 将匹配到的字符串数字转换为浮点数
        number = float(match.group())
        return number
    else:
        # 如果没有匹配到数字，返回 None 或者其他默认值
        return None

# 测试多个字符串
strings = ["2 分钟前", "5.5 小时前", "昨天", "100.1 秒前"]

for s in strings:
    number = extract_number_from_string(s)
    print(f"从字符串 '{s}' 中提取的数字为: {number}")

# 输出:
# 从字符串 '2 分钟前' 中提取的数字为: 2.0
# 从字符串 '5.5 小时前' 中提取的数字为: 5.5
# 从字符串 '昨天' 中提取的数字为: None
# 从字符串 '100.1 秒前' 中提取的数字为: 100.1