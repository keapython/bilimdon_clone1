from pydantic import BaseModel
from datetime import date

class UserSchema(BaseModel):
    id:int
    first_name: str
    last_name: str
    username: str
    birthdate: date


#     dummy_data={
#     "id": 1,
#     "first_name": "John",
#     "last-name": "Doe",
#     "username": 1,
#     "birthdate": date(year=200, month=1, day=1)
# }

# user = UserSchema(**dummy_data)
# user_dict = user.model.dump()
# user_dict['is_user'] = True
# print(user_dict)