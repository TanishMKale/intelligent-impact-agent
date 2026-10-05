from app.db import get_connection


def get_requirements_for_modules(module_ids):
    """
    Return all ACTIVE requirements that belong to the given modules.
    module_ids: list like ["MOD-PAY-ONB", "MOD-CBS-CIF"]
    """
    if not module_ids:
        return []

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT requirement_id, application_id, module_id, description
        FROM requirement
        WHERE module_id = ANY(%s)
          AND status = 'ACTIVE'
        ORDER BY requirement_id
    """
    cur.execute(query, (module_ids,))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return [dict(row) for row in rows]


def get_mapped_test_cases(requirement_ids):
    """
    Return test cases explicitly mapped to the given requirements
    (uses the requirement_testcase_map table).
    """
    if not requirement_ids:
        return []

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT
            t.test_case_id,
            t.application_id,
            t.module_id,
            t.scenario,
            m.requirement_id
        FROM requirement_testcase_map m
        JOIN test_case t ON t.test_case_id = m.test_case_id
        WHERE m.requirement_id = ANY(%s)
        ORDER BY t.test_case_id
    """
    cur.execute(query, (requirement_ids,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "test_case_id": row["test_case_id"],
            "application_id": row["application_id"],
            "module_id": row["module_id"],
            "scenario": row["scenario"],
            "mapped_requirement_id": row["requirement_id"],
            "evidence_type": "CONFIRMED_TRACEABILITY",
        })
    return results

def get_application_criticality_map():
    """Returns something like {"APP-PAY": "Critical", "APP-CRM": "High"}"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT application_id, criticality FROM application")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = {}
    for row in rows:
        result[row["application_id"]] = row["criticality"]
    return result

def get_module_by_id(module_id):
    """Returns module + application info, or None if the module does not exist."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.module_id, m.name AS module_name,
               a.application_id, a.name AS application_name
        FROM module m
        JOIN application a ON a.application_id = m.application_id
        WHERE m.module_id = %s
    """, (module_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row is None:
        return None
    return dict(row)