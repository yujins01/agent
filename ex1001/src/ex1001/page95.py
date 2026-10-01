# from typing import TypedDict

# class User(TypedDict):
#     id: int
#     name: str
#     email: str

# user1: User={
#     'id': 1,
#     'name': 'nayeon',
#     'email': 'example@gmail.com'
# }
# print(user1)

from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

user_data = {
    'id': 1,
    'name': '길동',
    'email': 'ex@gmail.com'
}

user1 = User(**user_data)
print(user1)