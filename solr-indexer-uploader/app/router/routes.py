from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from os import getcwd, remove
from utils.solrClient import clientSorl
from utils.pdfDataExtractor import pdfDataExtractor
from fastapi.exceptions import HTTPException
from langdetect import detect


router = APIRouter()

Path_File = getcwd() + "/"


@router.post('/upload')
async def upload_document(file: UploadFile = File(...)):
    try:

        pdfDataExtractorObject = pdfDataExtractor()

        with open(Path_File + file.filename, "wb") as myfile:
            content = await file.read()
            myfile.write(content)
            myfile.close()

        if detect(pdfDataExtractorObject.get_text_content_no_white_space(Path_File + file.filename)) != "es":
            print("Unsupported language for document")
            remove(Path_File + file.filename)
            raise Exception("Unsupported language for document")

        client = clientSorl()
        client.submit_document(Path_File + file.filename, file.filename)

        return JSONResponse(content={"message": "success"}, status_code=200)
    except BaseException as ex:
        raise HTTPException(400, detail=str(ex))


@router.get('/file/{name_document}')
def get_document(name_document: str):
    return FileResponse(Path_File + name_document)


@router.get("/download/{name_document}")
def download_file(name_document: str):
    return FileResponse(Path_File + name_document, media_type="application/octet-stream", filename=name_document)
