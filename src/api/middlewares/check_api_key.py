from fastapi import HTTPException, Header
import os

api_key_secret = os.environ.get("api_key_secret")

"""
Guard to prevent access without api-key header
TODO -> Should change for OAuth2
"""
async def check_api_key(api_key: str = Header()):
    if api_key != api_key_secret:
        raise HTTPException(status_code=401, detail="Invalid api key")
