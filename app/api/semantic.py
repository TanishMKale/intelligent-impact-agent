from fastapi import APIRouter
from app.services import semantic_service

router = APIRouter(prefix="/semantic", tags=["semantic"])


@router.post("/reindex")
def reindex():
    return semantic_service.reindex_all_test_cases()