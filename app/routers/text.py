
from fastapi import APIRouter
from ..util.embeddingDB import EmbeddingDB

db = EmbeddingDB(init_openai=False)
db.read("chk.json")

router = APIRouter()

@router.get("/text/")
async def read_text(text_id: int):
    return {"text_id": text_id}

@router.get("/text/{text_id}")
async def read_text(text_id: int):
    return {"id":text_id,"text": db.get_text(text_id)}
