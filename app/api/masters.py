from fastapi import APIRouter
from app.db import get_connection

router = APIRouter(prefix="/masters", tags=["masters"])


@router.get("/applications")
def list_applications():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.application_id, a.name AS application_name,
               a.criticality AS application_criticality,
               m.module_id, m.name AS module_name,
               m.criticality AS module_criticality
        FROM application a
        JOIN module m ON m.application_id = a.application_id
        ORDER BY a.application_id, m.module_id
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/dependencies")
def list_dependencies():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT dependency_id, source_module_id, target_module_id,
               relationship_type, description, criticality
        FROM application_dependency
        ORDER BY dependency_id
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(row) for row in rows]
