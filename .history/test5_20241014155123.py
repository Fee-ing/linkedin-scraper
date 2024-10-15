import requests

# 定义请求的URL
url = "http://172.30.20.244/pull-msg"

# 定义查询参数
params = {
    "kh_avatar": "test",
    "kh_name": "test",
    "kh_guojia": "test",
    "kh_gz": "test",
    "kh_time": "test",
    "kh_url": "test"
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