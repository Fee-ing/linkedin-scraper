import re

def get_time_number(text):
        numbers_str = re.findall(r'-?\d+(\.\d+)?', text)
        numbers = [float(num_str) if '.' in num_str else int(num_str) for num_str in numbers_str]
        # num = numbers[0] if numbers else 0
        # if "秒" in text or "s" in text:
        #     num = num * 10
        # elif "分钟" in text or "m" in text:
        #     num = num * 100
        # elif "小时" in text or "h" in text:
        #     num = num * 1000
        return numbers


print(get_time_number("2 分钟前"))