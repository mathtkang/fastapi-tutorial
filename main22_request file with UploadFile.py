from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_file(
    # file: bytes = File()
    files: List[bytes] = File()
):
    return {
        # "file_size": len(file)
        "file_sizes": [len(file) for file in files]
    }


@app.post("/uploadfile/")
async def create_upload_file(
    # file: UploadFile
    files: List[UploadFile]
    ):
    return {
        # "filename": file.filename
        "filenames": [file.filename for file in files]
    }

'''
'UploadFile'의 attributes
- filename : str  (e.g. image.jpg)
- content_type : str  (e.g. image/jpeg)
- file : SpooledTemporaryFile

UploadFile의 async methods (using the internal SpooledTemporaryFile)
- write(data) : data(str or bytes)를 파일에 작성
- read(size) : 파일의 size(int)를 읽음
- seek(offset) : 파일 내 offset(int) 위치의 바이트로 이동
- close() : 파일 닫음
'''


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)