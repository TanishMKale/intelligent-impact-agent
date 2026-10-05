from app.db import get_connection


def get_impacted_modules(source_module_id, depth=2):
    """
    Walk the application_dependency table starting from source_module_id.
    depth=0 -> nothing (only the source itself)
    depth=1 -> direct dependencies
    depth=2 -> direct + one more hop
    Returns a list of impacted modules (source module not included).
    """
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT
            d.target_module_id,
            d.relationship_type,
            d.description,
            m.name AS module_name,
            a.application_id,
            a.name AS application_name
        FROM application_dependency d
        JOIN module m ON m.module_id = d.target_module_id
        JOIN application a ON a.application_id = m.application_id
        WHERE d.source_module_id = %s
    """

    visited = {source_module_id}      # modules we already saw (avoids duplicates and cycles)
    results = []
    current_level = [(source_module_id, [source_module_id])]   # (module, path taken to reach it)

    for level in range(1, depth + 1):
        next_level = []

        for module_id, path in current_level:
            cur.execute(query, (module_id,))
            rows = cur.fetchall()

            for row in rows:
                target_id = row["target_module_id"]

                if target_id in visited:
                    continue          # already found, skip

                visited.add(target_id)
                new_path = path + [target_id]

                results.append({
                    "module_id": target_id,
                    "module_name": row["module_name"],
                    "application_id": row["application_id"],
                    "application_name": row["application_name"],
                    "relationship_type": row["relationship_type"],
                    "description": row["description"],
                    "depth": level,
                    "path": new_path,
                    "evidence_type": "CONFIRMED_DEPENDENCY",
                })
                next_level.append((target_id, new_path))

        current_level = next_level

    cur.close()
    conn.close()
    return results