from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["search"])
async def search(keyword: str = None):
    if keyword:
        return {"keyword": keyword, "code": 0}
    else:
        return {"code": 1, "msg": "require keyword"}

