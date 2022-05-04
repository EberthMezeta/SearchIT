from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from os import getcwd
from utils.solr_client import SolrClient
from fastapi.exceptions import HTTPException
from langdetect import detect
import pdfplumber
import io

router = APIRouter()

Path_File = getcwd() + "/"


@router.post('/upload')
async def upload_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        buffer = io.BytesIO(content)

        with pdfplumber.open(buffer) as pdf:
            if detect(pdf.pages[0].extract_text()) != "es":
                print("Unsupported language for document")
                raise Exception("Unsupported language for document")

        with open(Path_File + file.filename, "wb") as myfile:
            myfile.write(content)
            myfile.close()

        client = SolrClient()
        client.submit_document(Path_File + file.filename, file.filename)

        return JSONResponse(content={"message": "success"}, status_code=200)
    except BaseException as ex:
        raise HTTPException(400, detail=str(ex))


@router.get('/file/{name_document}')
def get_document(name_document: str):
    try:
        return FileResponse(Path_File + name_document)
    except BaseException as ex:
        raise HTTPException(400, detail=str(ex))


@router.get("/download/{name_document}")
def download_file(name_document: str):
    try:
        return FileResponse(Path_File + name_document, media_type="application/octet-stream", filename=name_document)
    except BaseException as ex:
        raise HTTPException(400, detail=str(ex))
