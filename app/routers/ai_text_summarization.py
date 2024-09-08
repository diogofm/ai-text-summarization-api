from fastapi import APIRouter
from pydantic import BaseModel

from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser


class Text(BaseModel):
    text: str


class Summary(BaseModel):
    summary: str


router = APIRouter()

model = ChatVertexAI(model="gemini-1.5-flash")
parser = StrOutputParser()


@router.post("/summarize/", response_model=Summary, tags=["ai"])
async def summarize(text: Text):
    messages = [
        SystemMessage(
            content="You are a text summarizer specialist. Answer only with the summary of the text provided by the user."
        ),
        HumanMessage(content=text.text),
    ]

    chain = model | parser

    result = chain.invoke(messages)

    return {"summary": result}
