from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()

'''
['/docs' 에서 example values 로 표현된다.]
1. pydantic 'schema_extra'
2. 'Field' additional arguments
3. function 'Body()' with example
4. function 'Body()' with multiple example
'''


class Item(BaseModel):
    '''case1) using pydantic schema_extra'''
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    class Config:
        schema_extra = {
            # example request data
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }

    '''case2) using 'Field' additional arguments'''
    name: str = Field(example="Foo")
    description: str | None = Field(
        default=None, 
        example="A very nice Item"  # example request data
    )
    price: float = Field(example=35.4)
    tax: float | None = Field(default=None, example=3.2)


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    '''1. 2.'''
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        # example request data
        # case3) using 'Body()' with example
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
        # case4) using 'Body()' with multiple example
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    
    results = {"item_id": item_id, "item": item}
    return results



