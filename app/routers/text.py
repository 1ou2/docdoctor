
from fastapi import APIRouter,Depends
from typing import Annotated
from ..util.embeddingDB import EmbeddingDB
from ..util.token import verify, Token

db = EmbeddingDB(init_openai=False)
db.read("chk.json")

router = APIRouter(prefix="/v1.0",dependencies=[Depends(verify)])

@router.get("/textid/")
async def getid(text_id: int):
    return {"text_id": text_id}

@router.get("/text/filter")
async def similarity(t: str):
    result = db.filter(t)
    print(result)
    response = dict(result)
    
    return response


@router.get("/text/{text_id}")
async def read_text(text_id: int):
    return {"id":text_id,"text": db.get_text(text_id)}

