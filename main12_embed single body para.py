from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int, 
    item: Item = Body(embed=True)  # declare extra body parameters
):
    results = {"item_id": item_id, "item": item}
    return results



'''
NOT

{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}

BUT

{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
'''