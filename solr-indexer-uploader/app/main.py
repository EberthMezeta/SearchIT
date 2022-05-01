from fastapi import FastAPI
from router import routes
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI(docs_url="/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost',
                port=8094, reload=True, debug=True)
