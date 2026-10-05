from fastapi import APIRouter, HTTPException

from app.models.schemas import AnalyzeRequest
from app.agents.orchestrator import run_deterministic_analysis

router = APIRouter(prefix="/impact", tags=["impact"])


@router.post("/analyze")
def analyze(request: AnalyzeRequest):
    if not request.source_module_id:
        raise HTTPException(
            status_code=400,
            detail="source_module_id is required for now (AI extraction not built yet).",
        )

    try:
        return run_deterministic_analysis(
            cr_id=request.cr_id,
            source_module_id=request.source_module_id,
            depth=request.dependency_depth,
        )
    except ValueError as error:
        # controlled error, no stack trace to the client
        raise HTTPException(status_code=400, detail=str(error))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal error while running analysis.")