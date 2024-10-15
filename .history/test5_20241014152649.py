import requests

# 定义请求的URL
url = "https://api.example.com/data"

# 定义查询参数
params = {
    "page": 1,
    "limit": 10
}

# 发起GET请求并指定查询参数
response = requests.get(url, params=params)

# 检查请求是否成功
if response.status_code == 200:
    # 请求成功，处理响应数据
    data = response.json()
    print(data)
else:
    # 请求失败，打印状态码和错误信息
    print(f"请求失败，状态码：{response.status_code}")
    print(response.text)