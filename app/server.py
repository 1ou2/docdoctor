from fastapi import FastAPI,Request,Form,Depends
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.embeddingDB import EmbeddingDB
from typing import Annotated
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


db = EmbeddingDB()
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

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class Text(BaseModel):
    id: int
    data: str | None = None

# templates directory
templates = Jinja2Templates(directory="templates")
# static files : css, img
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/admin/")
async def admin(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

# Test page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request,qr:str):
    data = {
        "page": "Home page: hello!" +qr
    }
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request):
    data = {
        "page": "no results"
    }
    return templates.TemplateResponse("search.html", {"request": request, "data": data})


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}

@app.get("/v1.0/text/")
async def read_text(text_id: int):
    return {"text_id": text_id}

@app.get("/v1.0/text/{text_id}")
async def read_text(text_id: int):
    return {"id":text_id,"text": db.get_text(text_id)}

@app.post("/ptext/")
async def read_ptext(text_id: int):
    return {"text_id": db.get_text(text_id)}

@app.post("/search", response_class=HTMLResponse)
async def search_text(request: Request,text_id: Annotated[int, Form()]):
    return templates.TemplateResponse("search.html", {"request": request, "data": db.get_text(text_id)})



#@app.get("/filter/{embedding}")
#async def filter(embedding: list):
#    return {"filter": db.filter(embedding)}
