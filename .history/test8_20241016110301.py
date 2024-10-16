class Test:
  def __init__(self, name, age):
        self.name = name
        self.age = age
        self.test()

  def test(self):
      return self.name
  
test = Test('aa', 13)
print(test)