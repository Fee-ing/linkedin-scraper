import requests

# # 定义请求的URL
# url = "http://172.30.20.244/pull-msg"

# # 定义查询参数
# params = {
#     "kh_avatar": "https://media.licdn.com/dms/image/v2/D5635AQFO9rnSNs8AmA/profile-framedphoto-shrink_200_200/profile-framedphoto-shrink_200_200/0/1714506740806?e=1729501200&v=beta&t=UunJ2jBo1DJuTFvAxo84fkur1x9sC1HSdeoyQIEgi5E",
#     "kh_name": "Kunwar Singh",
#     "kh_guojia": "Kunwar Singh",
#     "kh_gz": "经理, 襄理, 工资经理, 人力资源工资经理和人力资源共享服务经理职位",
#     "kh_time": "2 小时前",
#     "kh_url": "https://www.linkedin.com/in/kunwar-singh-078a5a123?miniProfileUrn=urn%3Ali%3Afsd_profile%3AACoAAB6XANwBGmR5r5c6Wu6AAwgukk2UWwvZHOo",
#     "type": "叶"
# }

# # 发起GET请求并指定查询参数
# response = requests.get(url, params=params)

# # 检查请求是否成功
# if response.status_code == 200:
#     # 请求成功，处理响应数据
#     data = response.json()
#     print(data)
# else:
#     # 请求失败，打印状态码和错误信息
#     print(f"请求失败，状态码：{response.status_code}")
#     print(response.text)



def getKeyword():
    response = requests.get("http://172.30.20.244/get-key-word")
    if response.status_code == 200:
        data = response.json()
        return data["data"]["key"]
    else:
        print(f"获取关键词失败，状态码：{response.status_code}")
        return None


keyword = getKeyword()
print(keyword)