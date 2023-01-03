from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

'''
What is Dependency Injectior?
DI를 위해 django framework에서는 Dictionary를 이용해서 주입하거나, DRF에서는 class를 이용해서 주입한다.
BUT 이는 framework에 강하게 종속적이기 때문에, 다른 프레임워크에서 사용하기는 어렵다.
Dependency Injectior는 프레임워크에 종속적이지 않은, python의 DI 프레임워크이다.
[link: https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html]

'''

# 1. DI def: endpoint(router)가 아닌 path operation의 역할 (그래서 decoration이 없음)
async def common_parameters(
    q: str | None = None, 
    skip: int = 0, 
    limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}  # type: dict


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons



fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# 2. DI class: dependency는 type도 되고 parameter도 된다. (typing is optional)
class CommonQueryParams:
    def __init__(
        self, 
        q: str | None = None, 
        skip: int = 0, 
        limit: int = 100
    ):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(
    commons: CommonQueryParams = Depends(CommonQueryParams)
    # commons: CommonQueryParams = Depends()  # for shortcut (이렇게 써도 fastapi는 알아들음)
):  # create 'instance' of CommonQueryParams class
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response



# 3. DI in path operation decorator
async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key  # but this return value is not passed to path operation decorator


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
