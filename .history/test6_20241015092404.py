obj = {
  "link": "http://"
}

arr = []
arr.append(obj)

if any(obj["link"] == "http:" for obj in arr) == True:
    print("11111")
else:
    print("2222")