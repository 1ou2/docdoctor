
from fastapi import APIRouter,Depends
from typing import Annotated
from ..util.embeddingDB import EmbeddingDB
from ..util.bearer import verify, Token

db = EmbeddingDB(init_openai=True)
db.read("chk.json")

router = APIRouter(prefix="/v1.0",dependencies=[Depends(verify)])

@router.get("/textid/")
async def getid(text_id: int):
    return {"text_id": text_id}

@router.post("/text/similar")
@router.get("/text/similar")
async def similarity(t: str):
    result = db.get_similar(t)
    print(result)
    
    return result[0]


@router.get("/text/{text_id}")
async def read_text(text_id: int):
    return {"id":text_id,"text": db.get_text(text_id)}

