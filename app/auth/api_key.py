from fastapi import Request, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from dotenv import load_dotenv
import os

load_dotenv()

ISIS_API_KEY = os.getenv("API_KEY")

def api_key_auth(request: Request):
    api_key = request.headers.get("Api-Key")
    if api_key != ISIS_API_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid Api Key"
        )
    return api_key
