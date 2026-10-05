import uuid
from datetime import datetime, timezone

from app.services.dependency_service import get_impacted_modules
from app.services.traceability_service import (
    get_requirements_for_modules,
    get_mapped_test_cases,
    get_application_criticality_map,
    get_module_by_id,
)
from app.services.scoring_service import calculate_score


def run_deterministic_analysis(cr_id, source_module_id, depth=2):
    started_at = datetime.now(timezone.utc)
    warnings = []

    # 1. validate the source module against the master (never trust input blindly)
    source = get_module_by_id(source_module_id)
    if source is None:
        raise ValueError(f"Unknown source module: {source_module_id}")

    # 2. dependency lookup
    impacted = get_impacted_modules(source_module_id, depth)
    if not impacted:
        warnings.append("No cross-application dependencies found in dependency master.")

    # info about every module in scope (source = depth 0)
    module_info = {
        source_module_id: {"depth": 0, "relationship_type": None, "path": [source_module_id]}
    }
    impacted_applications = []
    for item in impacted:
        module_info[item["module_id"]] = {
            "depth": item["depth"],
            "relationship_type": item["relationship_type"],
            "path": item["path"],
        }
        impacted_applications.append({
            "application_id": item["application_id"],
            "application_name": item["application_name"],
            "module_id": item["module_id"],
            "module_name": item["module_name"],
            "relationship_type": item["relationship_type"],
            "depth": item["depth"],
            "dependency_path": item["path"],
            "reason": f"{item['relationship_type']}: {item['description']}",
            "evidence_type": "CONFIRMED_DEPENDENCY",
        })

    # 3. requirements in source + impacted modules
    requirements = get_requirements_for_modules(list(module_info.keys()))
    req_ids = [req["requirement_id"] for req in requirements]

    # 4. mapped test cases (one entry per test case, even if mapped twice)
    mapped_rows = get_mapped_test_cases(req_ids)
    mapped_test_cases = {}
    for row in mapped_rows:
        tc_id = row["test_case_id"]
        if tc_id not in mapped_test_cases:
            mapped_test_cases[tc_id] = {
                "test_case_id": tc_id,
                "application_id": row["application_id"],
                "module_id": row["module_id"],
                "scenario": row["scenario"],
                "mapped_requirements": [],
            }
        mapped_test_cases[tc_id]["mapped_requirements"].append(row["mapped_requirement_id"])

    # 5. score and explain every test case
    criticality_map = get_application_criticality_map()
    ranked = []
    for tc in mapped_test_cases.values():
        info = module_info.get(tc["module_id"])
        depth_of_tc = info["depth"] if info else None
        criticality = criticality_map.get(tc["application_id"], "Low")

        score = calculate_score(True, depth_of_tc, 0.0, criticality)

        evidence = ["CONFIRMED_TRACEABILITY"]
        if depth_of_tc is not None and depth_of_tc >= 1:
            evidence.append("CONFIRMED_DEPENDENCY")

        reqs_text = ", ".join(tc["mapped_requirements"])
        if depth_of_tc == 0:
            reason = f"Mapped to {reqs_text}; test belongs to the changed module."
        else:
            reason = (f"Mapped to {reqs_text}; module reached via "
                      f"{info['relationship_type']} dependency.")

        ranked.append({
            "test_case_id": tc["test_case_id"],
            "application_id": tc["application_id"],
            "module_id": tc["module_id"],
            "scenario": tc["scenario"],
            "score": score["final_score"],
            "label": score["label"],
            "recommendation": score["recommendation"],
            "default_included": score["default_included"],
            "score_components": score["components"],
            "evidence": evidence,
            "reason": reason,
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)

    warnings.append("Semantic search not enabled yet (mapped test cases only).")

    finished_at = datetime.now(timezone.utc)
    return {
        "run_id": str(uuid.uuid4()),
        "processing": {
            "started_at": started_at.isoformat(),
            "duration_ms": int((finished_at - started_at).total_seconds() * 1000),
            "dependency_depth": depth,
        },
        "change_extraction": {
            "cr_id": cr_id,
            "source_application": source["application_name"],
            "source_module": source["module_name"],
            "source_module_id": source_module_id,
            "note": "Source supplied by caller. AI extraction not built yet.",
        },
        "impacted_applications": impacted_applications,
        "impacted_requirements": requirements,
        "mapped_test_cases": list(mapped_test_cases.values()),
        "semantic_test_cases": [],
        "ranked_test_cases": ranked,
        "warnings": warnings,
    }