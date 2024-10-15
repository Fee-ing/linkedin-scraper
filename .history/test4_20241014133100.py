import re

def extract_and_convert_numbers(input_string):
    """
    从字符串中提取所有数字，并将它们转换成整数或浮点数。
    
    参数:
    input_string (str): 输入的字符串。
    
    返回:
    list: 包含提取出来的数字的列表。
    """
    # 使用正则表达式匹配所有的数字
    numbers_str = re.findall(r'-?\d+(\.\d+)?', input_string)
    
    # 使用列表推导式将字符串数字转换成整数或浮点数
    numbers = [float(num_str) if '.' in num_str else int(num_str) for num_str in numbers_str]
    
    return numbers

# 测试函数
input_string = "ee"
result = extract_and_convert_numbers(input_string)
print(result[0])  # 输出: [123.45, 50, 0.9]