from typing import Optional
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    cr_id: str
    title: str
    description: str
    # Temporary: caller supplies the source module until AI extraction is built
    source_module_id: Optional[str] = None
    dependency_depth: int = Field(default=2, ge=0, le=2)
    top_k_semantic: int = Field(default=10, ge=1, le=50)