from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

'''
- Convert the output data to its type declaration.
- 데이터 검증
- OpenAPI 경로 작업에서 응답에 대한 json 스키마 추가
- Will be used by the automatic documentation systems.
- Will limit the output data to that of the model. We'll see how that's important below.
= 출력 데이터를 모델의 데이터로 제한!
'''

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5  # default value
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    # "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]

'''
request: foo
{
    "name": "Foo",
    "price": 50.2
}

request: bar
{
    "name": "Bar",
    "description": "The bartenders",
    "price": 62,
    "tax": 20.2
}

request: baz
{
    "name": "Baz",
    "description": None,
    "price": 50.2,
    "tax": 10.5,
    "tags": []
}
'''
@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]




class UserIn(BaseModel):
    # Don't do this in production!
    username: str
    password: str  # danger
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    # FastAPI will take care of filtering out all the data that is not declared in the output model (using Pydantic)
    return user

