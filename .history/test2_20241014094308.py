import json
import random

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def to_dict(self):
        """将对象转换为字典"""
        return {
            'name': self.name,
            'age': self.age
        }

# 创建一个 Person 对象
person = Person("Alice", 30)

# 将对象转换为字典
person_dict = person.to_dict()

# 使用 json.dumps 将字典转换为 JSON 字符串
person_json = json.dumps(person_dict, indent=4)

# 打印 JSON 字符串
print(person_json)

# 创建一个包含多个 Person 对象的列表
people = [
    Person("Alice", 30),
    Person("Bob", 25),
    Person("Charlie", 35)
]

# 将列表中的每个对象转换为字典
people_dicts = [person.to_dict() for person in people]

# 将列表转换为 JSON 字符串
people_json = json.dumps(people_dicts, indent=4)

# 打印 JSON 字符串
print(people_json)

m = 1
n = 10

random_number = random.randint(m, n)
print(random_number)  # 输出 m 到 n 之间的一个随机整数


# callycyddea@mail.ru:sPq1yrQgd0?:callycyddea@mail.ru:sPq1yrQgd0?:linkedin.com/in/yuliya-ermakova-7aa3a1330

# https://media.licdn.com/dms/image/v2/D4D35AQELwnlNK8DStA/profile-framedphoto-shrink_100_100/profile-framedphoto-shrink_100_100/0/1727074239608?e=1729476000&v=beta&t=BG_Skvfqz-v2OsxopYtEfJyQLf0M9KNHm47ktIIt6YY
# https://media.licdn.com/dms/image/v2/D4D03AQHC738N67wupg/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1695479523956?e=1734566400&v=beta&t=NKvvu8NhgDgBl0ypyP--60qZjVIuFG1B_vQaCpSzMgw