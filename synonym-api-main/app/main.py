
import uvicorn
from fastapi import FastAPI
from app import synonym_helper

app = FastAPI(docs_url="/")

@app.get("/spa")
async def spa_synonym(word:str):
    return synonym_helper.get_synonyms(word, "spa")

@app.get("/eng")
async def eng_synonym(word:str):
    return synonym_helper.get_synonyms(word, "eng")

if __name__=="__main__":
    uvicorn.run("main:app",host='localhost', port=8091, reload=True, debug=True)
