from fastapi import FastAPI
from router import routes

import uvicorn


app = FastAPI(docs_url="/")

app.include_router(routes.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost',
                port=8094, reload=True, debug=True)
