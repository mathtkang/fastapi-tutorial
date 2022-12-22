from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel

app = FastAPI()


'''
When using custom headers to the HTTP error (with HTTPException)
-> generally not needed, BUT in case you needed it for an advanced scenario OR some types of security.
'''

items = {"foo": "The Foo Wrestlers"}

@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},  # custom headers
        )
    return {"item": items[item_id]}




# 1. 함수 안에 if-raise구문으로 error를 발생해도 되지만,
@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)  
    return {"unicorn_name": name}


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

# 2. 'exception_handler' to decorate the exception handler 를 이용해서 error 발생도 가능
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )
'''
{"message": "Oops! yolo did something. There goes a rainbow..."}
'''

# 1.
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


# 2.
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# 'RequestValidationError' contains the body it received with invalid data.
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # return PlainTextResponse(str(exc), status_code=400)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "detail": exc.errors(), 
            "body": exc.body
        }),
    )

class Item(BaseModel):
    title: str
    size: int


@app.post("/items/")
async def create_item(item: Item):
    return item

'''
if you go to '/items/foo', instead of getting the default JSON error 
with

{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
'''