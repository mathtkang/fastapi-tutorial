import time

from fastapi import FastAPI, Request

app = FastAPI()


# Create a middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # request의 수행시간 측정
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # custom proprietary header에 넣어서 client(user)에게 전달
    response.headers["X-Process-Time"] = str(process_time)
    return response
