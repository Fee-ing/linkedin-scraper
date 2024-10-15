import json

aa = {
  "b": "cc"
}

 print(json.dumps(aa.to_dict(), indent=4))