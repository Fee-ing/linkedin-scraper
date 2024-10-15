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
