from fastapi import HTTPException, Header

api_key_secret = "asdfds93wsdf"


async def check_api_key(api_key: str = Header()):
    if api_key != api_key_secret:
        raise HTTPException(status_code=401, detail="Invalid api key")
