from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


# 1. Tags in path operation decorator
@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]

# 3. summary and description in path operation decorator
# 4. Description from docstring (description이 길어지는 경우, '/docs'에서도 보여야하는 경우)
# 5. Response description (작성하지 않아도 fastapi가 자동으로 생성함)
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    # description="Create an item with all the information, name, description, price, tax and a set of unique tags",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:  

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item

    => 해당 주석은, 대화형 문서(docs)에서 볼 수 있음
    """
    return item

# 2. Tags with Enums
class Tags(Enum):
    items = "items"
    users = "users"

@app.get("/items/", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumbus"]


@app.get("/users/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]


# 6. Deprecate a path operation(해당 경로를 중지해야하지만, 코드상 제거하지 않은 경우) -> docs에서 약간 흐리게 나옴
@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]