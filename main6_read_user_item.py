from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
):
    # needy is 'required query parameter'
    # 'optional query parameter'를 표현할 때 Union을 사용
    item = {"item_id": item_id, "needy": needy}
    return item
