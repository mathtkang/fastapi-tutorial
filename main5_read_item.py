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
