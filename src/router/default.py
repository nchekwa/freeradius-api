from fastapi import APIRouter

from settings import API_BASE_URL

router = APIRouter()


@router.get("/", include_in_schema=False)
def read_root():
    return {"Welcome!": f"API docs is available at {API_BASE_URL}/docs"}
