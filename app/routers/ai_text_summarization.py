from fastapi import APIRouter
from pydantic import BaseModel

from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

MIN_NUMBER_OF_WORDS_WORTH_TO_SUMMARIZE = 10


class Text(BaseModel):
    text: str


class Summary(BaseModel):
    summary: str


router = APIRouter()

model = ChatVertexAI(model="gemini-1.5-flash")
parser = StrOutputParser()


@router.post("/summarize/", response_model=Summary, tags=["ai"])
async def summarize(text: Text):
    # Check if text is empty to avoid calling the LLM API.
    if text.text == "" or text.text.isspace():
        return {"summary": "Text is empty. Nothing to summarize."}

    if len(text.text.split(" ")) <= MIN_NUMBER_OF_WORDS_WORTH_TO_SUMMARIZE:
        return {"summary": "Text not long enough. Nothing to summarize."}

    messages = [
        SystemMessage(
            content="You are a text summarizer specialist. Answer only with the summary of the text provided by the user."
        ),
        HumanMessage(content=text.text),
    ]

    chain = model | parser

    result = chain.invoke(messages)

    return {"summary": result}
