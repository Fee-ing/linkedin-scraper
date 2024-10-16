class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 创建一个 Person 对象
person = Person("Alice", 30)

arr = []

arr.append(person)

# 直接访问 __dict__ 属性
print(person.__dict__)  # 输出: {'name': 'Alice', 'age': 30}
print(person)
print(arr[0].__dict__)