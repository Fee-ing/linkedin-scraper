obj = {
  "link": "http://"
}

arr = []
arr.append(obj)

def has_object_with_name(objects, name_to_find):
    for obj1 in objects:
        if obj1["link"] == name_to_find:
            return True
    return False

# 示例
print(has_object_with_name(obj, "http://"))  # 输出: True