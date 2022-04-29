from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from nltk.corpus import wordnet
import traceback

app = FastAPI(docs_url="/")

@app.get("/spa")
async def spa_synonym(word:str):
    try:
        results = []
        for syn in wordnet.synsets(word, lang=('spa')):
            for name in syn.lemma_names('spa'):
                results.append(name)
        return results
    except BaseException as ex:
        print(traceback.format_exc())
        return []

if __name__=="__main__":
    uvicorn.run("main:app",host='localhost', port=8091, reload=True, debug=True)