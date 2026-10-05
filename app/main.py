from fastapi import FastAPI

from app.api import impact, masters
from app.db import get_connection

app = FastAPI(title="Test Calibre - Impact Analysis Agent POC")

app.include_router(impact.router)
app.include_router(masters.router)


@app.get("/health")
def health():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "degraded", "database": "unreachable"}