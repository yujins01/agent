#클래스를 생성할 때, 클래스 초기화 사용

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person("에밀리",36)
print(p1.name)
print(p1.age)

#클래스 메서드 (액션)
class Person2:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print("내 이름은" + self.name)