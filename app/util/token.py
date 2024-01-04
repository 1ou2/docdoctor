from typing import Annotated
from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os

async def verify(token: str):
    load_dotenv()
    secured = os.getenv["SECURED_TOKEN"]
    if not secured:
        raise HTTPException(status_code=400, detail="Internal token error")
    if token != secured:
        raise HTTPException(status_code=400, detail="Invalid token")