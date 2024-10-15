import re

def get_time_number(text):
        match = re.search(r'\d+', text)
        num = 0
        if match:
            num = int(match.group())
        if "秒" in text or "s" in text:
            num = num * 10
        elif "分钟" in text or "m" in text:
            num = num * 100
        elif "小时" in text or "h" in text:
            num = num * 1000
        return num

# 测试
string = "8m • "
number = get_time_number(string)
print(number)  # 输出: 2