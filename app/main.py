import os

from fastapi import Depends, FastAPI
from .routers import ai_text_summarization
from .dependecies import get_api_key

from decouple import config


app = FastAPI(dependencies=[Depends(get_api_key)])

app.include_router(ai_text_summarization.router)

GOOGLE_API_KEY = config("GOOGLE_API_KEY")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


@app.get("/")
async def root():
    return {"message": "Welcome to the AI Text Summarization!"}
