from fastapi import APIRouter

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    dependencies=[]
)
