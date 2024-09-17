from fastapi import APIRouter

router = APIRouter()


# サンプルのAPI
@router.get("/hello", tags=["hello"])
async def hello():
    return {"message": "hello world!"}
