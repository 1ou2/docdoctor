from fastapi import FastAPI,Request,Form,Depends

from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.embeddingDB import EmbeddingDB
from typing import Annotated
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


db = EmbeddingDB(init_openai=False)
db.read("chk.json")
app = FastAPI()

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://localhost:8000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# authenticate API
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@app.get("/admin/")
async def admin(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

# Test page
@app.get("/")
async def home():
    return {
        "page": "Home page: hello!" 
    }


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username, "password":password}

@app.get("/v1.0/text/")
async def read_text(text_id: int):
    return {"text_id": text_id}

@app.get("/v1.0/text/{text_id}")
async def read_text(text_id: int):
    return {"id":text_id,"text": db.get_text(text_id)}


