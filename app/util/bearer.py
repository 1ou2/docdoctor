from typing import Annotated
from fastapi import Header, HTTPException,Depends,status
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str


# verify that the request comes with a valid access Token
#
# Required Headers
# - Accept: application/json
# - Authorization: Bearer xxxx

async def verify(token: Annotated[Token, Depends(oauth2_scheme)]):
    load_dotenv()
    secured = os.getenv("SECURED_TOKEN")
    if not secured:
        raise HTTPException(status_code=400, detail="Internal token error")
    
    if token != secured:
        raise HTTPException(status_code=400, detail="Invalid token")