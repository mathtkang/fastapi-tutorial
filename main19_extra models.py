from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    # Input model : be able to have a password
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    # output model : should not have a password
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    # database model : probably need to have a hashed password
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


'''About Dictinary'''
# 1. create pydantic object
user_in = UserIn(
    username="john", 
    password="secret", 
    email="john.doe@example.com"
)
user_dict = user_in.dict()
'''
print(user_dict)
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
'''

# 2. unwrapping
UserInDB(**user_dict)  # writing
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)  # result

# 3. A Pydantic model from the contents of another
UserInDB(**user_in.dict(), hashed_password=hashed_password) # writing
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
) # result
