from typing import Union, List, Dict

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

'''
what is 'typing.Union'?
'Union[X, Y]' is equivalent to X | Y and means either X or Y.
It will be defined in OpenAPI with 'anyOf'.


'''


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get(
    "/items/{item_id}", 
    # response_model=Union[PlaneItem, CarItem]  # python 3.6
    response_model=PlaneItem | CarItem  # python 3.10
) 
async def read_item(item_id: str):
    return items[item_id]
