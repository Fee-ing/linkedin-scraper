obj = {
  "link": "http://"
}

arr = []
arr.append(obj)

def has_object_with_name_v2(arr, str):
    return any(obj["link"] == str for obj in arr)

# 示例
print(has_object_with_name_v2(arr, "http:"))  # 输出: True