from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}

'''
Form is a class that inherits directly from Body.

when using 'Form'?
json 대신에 form field를 받았다면, Form 클래스로 처리 가능

HTML forms (<form></form>)은 데이터를 "special"하게 encoding해서 보내준다. -> 이것은 json과 다르다.
fastapi는 해당 데이터를 자동 변환해주어, 적절하게 변수 매칭을 해준다.
'''