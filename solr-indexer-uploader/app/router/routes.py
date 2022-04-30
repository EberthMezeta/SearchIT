from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from os import getcwd
from utils.solrClient import clientSorl


router = APIRouter()

Path_File = getcwd() + "/"


@router.post('/upload')
async def upload_document(file: UploadFile = File(...)):
    with open(Path_File + file.filename, "wb") as myfile:
        content = await file.read()
        myfile.write(content)
        myfile.close()

    client = clientSorl()
    client.submit_document(Path_File + file.filename)

    return JSONResponse(content={"message": "success"}, status_code=200)


@router.get('/file/{name_document}')
def get_document(name_document: str):
    return FileResponse(Path_File + name_document)


@router.get("/download/{name_document}")
def download_file(name_document: str):
    return FileResponse(Path_File + name_document, media_type="application/octet-stream", filename=name_document)
