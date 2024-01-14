from fastapi import APIRouter,Depends,UploadFile,File
from typing import Annotated
from ..util.embeddingDB import EmbeddingDB
from ..util.search import Query
from ..util.bearer import verify, Token
from pydantic import BaseModel

DB = EmbeddingDB(init_openai=True)
DB.read("db2.json")

class DbModel(BaseModel):
    name:str
    filetype:str|None=".json"

router = APIRouter(prefix="/v1.0",dependencies=[Depends(verify)])

@router.get("/db/describe")
async def describe():
    return {"version": "1.0.0","name":DB.dbname,"columns":list(DB.df.columns),"size":len(DB.df)}


@router.post("/db/load")
async def load(newdb:DbModel):
    
    name = newdb.name
    DB.read(name)
    
    return {"dbname":name}

@router.post("/db/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()

        #with open(file.filename, 'wb') as f:
        #    f.write(contents)
        #ing = Ingester(filename=file.filename)
        #ing.add_text(contents)
        #data = ing.create_data(self)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}