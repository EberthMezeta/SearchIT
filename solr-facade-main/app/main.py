
import json
import traceback
from app.constants import solr_host, params, headers, request_object
from app.tokenizer import tokenizer
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import requests


app = FastAPI(docs_url="/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/query")
async def query_endpoint(query: str):
    try:
        first_response = requests.post(f"http://{solr_host}:8983/solr/mycore/query{params}", headers=headers,
                                       data=json.dumps(request_object).replace("query_replacement", query).encode('utf-8'))
        first_response_json = first_response.json()
        if first_response_json['response']['numFound'] > 0:
            return {"results": [first_response_json]}

        tokenizer_object = tokenizer()

        fuzzy_query = tokenizer_object.get_clean_query(query)
        second_response = requests.post(f"http://{solr_host}:8983/solr/mycore/query{params}", headers=headers, data=json.dumps(
            request_object).replace("query_replacement", fuzzy_query).encode('utf-8'))
        second_response_json = second_response.json()
        return {"results": [second_response_json]}

    except BaseException as ex:
        return {"results": [traceback.format_exc()]}


@app.get("/suggest")
async def suggest_endpoint(query: str):
    try:
        suggest_response = requests.get(
            f"http://{solr_host}:8983/solr/mycore/suggest?suggest=true&suggest.build=true&suggest.dictionary=mySuggester&wt=json&suggest.q={query}".encode('utf-8'))
        suggest_json = suggest_response.json()
        return {"results": suggest_json}
    except BaseException as ex:
        return {"results": [traceback.format_exc()]}


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost',
                port=8093, reload=True, debug=True)
