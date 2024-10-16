import re

# 原始字符串
original_string = "2 小时前 • \n"

# 正则表达式模式
pattern = r"[\s\n•]+"

# 使用 re.sub 替换匹配的部分为空字符串
original_string = re.sub(pattern, "", original_string)

print(original_string)  # 输出: 2小时前