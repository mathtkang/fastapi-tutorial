from fastapi import FastAPI, Query
from pydantic import Required

app = FastAPI()

'''
Query()의 default 속성을 
    선언하면: '선택' 파라미터
    선언하지않으면: '필수' 파라미터
'''

@app.get("/items/optional/")
async def read_items_optional(
    q: str 
    | None = Query(default=None, min_length=3, max_length=50, regex="^fixedquery$")
):
    # Union[str, None](python ver.3.6) == str | None (python ver.3.10)
    # optional query parameter : 'None' or 'Query(default=None)' or 'Query(default="fixedquery")' 기본값이 있으면 매개변수도 선택사항이 됨
    # validations: min, max, regex..
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/required/")
async def read_items_required(q: str = Query(min_length=3)):
    # Query(default=..., min_length=3) -> 줄임표 표시(default=...,): 해당 파라미터 필수
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results



@app.get("/items/usingpydantic")
async def read_items_using_pydantic(q: str = Query(default=Required, min_length=3)):
    # pydantic을 사용해서 Query(default=Required)로 명시 : 필수 파라미터
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/listandmultiple")
async def read_items_list_and_multiple(q: list[str] | None = Query(default=None)):
    # ex) http://localhost:8000/items/?q=foo&q=bar
    # define default value: Query(default=["foo", "bar"])
    # ex) http://localhost:8000/items
    query_items = {"q": q}
    return query_items


'''Deprecating parameters'''
@app.get("/items/deprecate")
async def read_items_deprecate(
    q: str
    | None = Query(
        default=None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,  # 사용하는 클라이언트가 있어서, (잠시동안) 그대로 두어야 하지만, 문서에서는 사용되지 않는 것으로 명확하게 표시
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results