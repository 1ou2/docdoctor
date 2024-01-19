
from fastapi import APIRouter,Depends
from typing import Annotated
from ..util.embeddingDB import EmbeddingDB
from ..util.search import Query
from ..util.bearer import verify, Token
from pydantic import BaseModel
from .db import DB

#db = EmbeddingDB(init_openai=True)
#db.read("chk.json")

class Question(BaseModel):
    question:str
    max_result:int|None=1

router = APIRouter(prefix="/v1.0",dependencies=[Depends(verify)])


@router.get("/textid/")
async def getid(text_id: int):
    return {"text_id": text_id}

@router.post("/text/similar")
async def similarity_post(q:Question):
    
    res = DB.get_similar(q.question,q.max_result)
    return {"responses":res}


@router.post("/text/ask")
async def similarity_post(q:Question):
    res = DB.get_similar(q.question,q.max_result)
    context = ""
    for r in res:
        if float(r['similarity']) > 0.8:
            context = context + r['text']
    query = Query()
    response = query.answer(q.question,context)
    return {"response":response,"similarity":res[0]['similarity']}

@router.get("/text/similar")
async def similarity(t: str):
    result = DB.get_similar(t)
    return result[0]


@router.get("/text/{text_id}")
async def read_text(text_id: int):
    return {"id":text_id,"text": DB.get_text(text_id)}

