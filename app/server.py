from fastapi import FastAPI,Request,Form,Depends,HTTPException, status

from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from typing import Annotated
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from .routers import text,user




app = FastAPI()
app.include_router(text.router)
app.include_router(user.router)

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

@app.get("/secret/")
async def secret():
    load_dotenv()
    secret=os.getenv("testsecret")
    return {
        "page": f"This is my secret -- {secret} --" 
    }

# Test page
@app.get("/")
async def home():
    return {
        "page": "Home page: hello!" 
    }


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    print(f"u:{username} -- p:{password}")
    return {"username": username, "password":password}




