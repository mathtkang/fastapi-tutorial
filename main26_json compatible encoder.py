from datetime import datetime
from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()

'''
데이터 자료형을 json과 호환되는 형태로 반환하는 경우 (ex. 데이터베이스에 저장해야하는 경우, dict, list,)
=> jsonable_encoder() 를 사용: 데이터 자료형을 json compatiable한 데이터로 바꿔주는 함수
'''

fake_db = {}

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
