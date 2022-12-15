from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    '''1. submodel'''
    # url: str
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: Union[float, None] = None
    # tags: list[str] = []  # list fields
    tags: set[str] = set()  # set type
    # image: Image | None = None  # use the submodel as a type
    images: list[Image] | None = None

class Offer(BaseModel):
    '''2. deeply nested models'''
    name: str
    description: str | None = None
    price: float
    items: list[Item]


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    '''1.'''
    results = {"item_id": item_id, "item": item}
    return results


@app.post("/offers/")
async def create_offer(offer: Offer):
    '''2.'''
    return offer

@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    '''3. Bodies of pure lists'''
    return images

@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    '''4. Bodies of arbitrary dict'''
    return weights




'''
# 1.
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}


# 2. if using 'pydantic > HttpUrl'
: image 속성이 list로 바뀜  (convert, validate, document, etc)
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
'''

