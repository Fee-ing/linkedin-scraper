obj = {
  "link": "http://"
}

arr = []
arr.append(obj)

def has_object_with_name(arr, val):
    for obj1 in arr:
        # print(val)
        # print(obj1["link"])
        if obj1["link"] == val:
            return True
    return False

# 示例
print(has_object_with_name(arr, "http:/"))  # 输出: True