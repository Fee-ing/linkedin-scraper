obj = {
  "linik": "http://"
}

arr = []
arr.append(obj)

def has_object_with_name_v2(objects, name_to_find):
    return any(obj.name == name_to_find for obj in objects)

# 示例
print(has_object_with_name_v2(obj, "http://"))  # 输出: True