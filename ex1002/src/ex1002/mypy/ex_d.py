class MyPerson:
    def __init__(self, name,age):
        self.name = name
        self.age = age

class Student(MyPerson):
    def __init__(self, name, age, school, grade):
        super().__init__(name, age)
        self.school = school
        self.grage = grade

st01 = Student("한석봉", 20, "호서대학교", 4)

print(st01.name)
print(st01.age)
print(st01.school)
print(st01.grage)