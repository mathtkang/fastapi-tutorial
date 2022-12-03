from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(
    q: str 
    | None = Query(default=None, min_length=3, max_length=50, regex="^fixedquery$")
):
    # Union[str, None](python ver.3.6) == str | None (python ver.3.10)
    # optional query parameter : 'None' or 'Query(default=None)
    # validations: min, max, regex..
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
