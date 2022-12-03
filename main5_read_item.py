from typing import Union
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [
    {"item_name": "Foo"}, 
    {"item_name": "Bar"}, 
    {"item_name": "Baz"}
]

'''query parameter'''
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    # /items/?skip=0&limit=10  (default)
    return fake_items_db[skip : skip + limit]



@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    # type of q as query parameter is str or None (default: None)
    # Union == anyOf : 두가지 타입 지정 가능, 첫번째 타입은 두 번째 타입보다 좀 더 중요하고 명시하고 싶은 타입으로 선언
    # optional query parameter를 표현할 때 Union을 사용
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item