from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# allowed origins list
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Authorization header, Cookie, etc.
    allow_methods=["*"],  # HTTP methods(POST, PUT, etc.)
    allow_headers=["*"],  # 특정 http headers 뿐만 아니라 모든 http headers 허락
)


# Use 'CORSMiddleware'
@app.get("/")
async def main():
    return {"message": "Hello World"}