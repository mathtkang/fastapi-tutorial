from typing import Union, List, Dict

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

'''
1. what is 'typing.Union'?
'Union[X, Y]' is equivalent to X | Y and means either X or Y.
It will be defined in OpenAPI with 'anyOf'.


2. what is 'typing.List'?
declare responses of lists of objects.

3. when using 'typing.Dict'?
pydantic.BaseModel을 사용하지 않고, 키와 값의 유형만 선언하는 경우
유효한 필드/속성 이름을 미리 모르는 경우

=> python 3.10 이상에서는 Union, List, Dict가 필요 없다.
'''


class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type = "car"

class PlaneItem(BaseItem):
    type = "plane"
    size: int

items1 = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

'''Union or anyOf'''
@app.get(
    "/items/{item_id}", 
    # response_model=Union[PlaneItem, CarItem]  # python 3.6
    response_model=PlaneItem | CarItem  # python 3.10
) 
async def read_item(item_id: str):
    return items1[item_id]



class Item(BaseModel):
    name: str
    description: str

items2 = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

'''List of models'''
@app.get(
    "/items/", 
    # response_model=List[Item]  # python 3.6
    response_model=list[Item]  # python 3.10
)
async def read_items():
    return items2



'''Response with arbitrary dict'''
@app.get(
    "/keyword-weights/", 
    # response_model=Dict[str, float]  # python 3.6
    response_model=dict[str, float]  # python 3.10
)
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}