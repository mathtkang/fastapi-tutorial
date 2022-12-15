from typing import Union
from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items_basic(
    # item_id: int = Path(title="The ID of the item to get"),
    # q: Union[str, None] = Query(default=None, alias="item-query"),
    q: str, 
    item_id: int = Path(title="The ID of the item to get"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results



'''
[Number validations]
gt: 크거나(greater than)
ge: 크거나 같은(greater than or equal)
lt: 작거나(less than)
le: 작거나 같은(less than or equal)
'''
@app.get("/items/{item_id}")
async def read_items_kwargs(
    *, 
    item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
    q: str,
    size: float = Query(gt=0, lt=10.5)
):
    # *가 첫번째 매개변수인 경우: 뒤에오는 매개변수들은 kwargs(key-value)키워드 인자이다.
    # ge=1 : item_idsms 1보다 '크거나 같은' 정수형 숫자
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results