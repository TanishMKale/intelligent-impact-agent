from app.services.dependency_service import get_impacted_modules
from app.services.traceability_service import (
    get_requirements_for_modules,
    get_mapped_test_cases,
    get_application_criticality_map,
)
from app.services.scoring_service import calculate_score

tests = [
    ("MOD-PAY-ONB", "CR-001 Payments Onboarding"),
    ("MOD-PAY-BEN", "CR-002 Payments Beneficiary"),
    ("MOD-CRM-COMM", "CR-003 CRM Comm Preferences"),
]

criticality_map = get_application_criticality_map()

for source_module, label in tests:
    print("=" * 60)
    print(label)

    # depth of every module: source = 0, impacted = 1 or 2
    impacted = get_impacted_modules(source_module, depth=2)
    depth_of_module = {source_module: 0}
    for item in impacted:
        depth_of_module[item["module_id"]] = item["depth"]

    requirements = get_requirements_for_modules(list(depth_of_module.keys()))
    req_ids = [req["requirement_id"] for req in requirements]
    test_cases = get_mapped_test_cases(req_ids)

    ranked = []
    for tc in test_cases:
        depth = depth_of_module.get(tc["module_id"])
        criticality = criticality_map.get(tc["application_id"], "Low")
        result = calculate_score(True, depth, 0.0, criticality)
        ranked.append((result["final_score"], tc, result))

    ranked.sort(key=lambda x: x[0], reverse=True)

    for score, tc, result in ranked:
        print(f"  {tc['test_case_id']}  {score:>5}  {result['label']:<8} {result['components']}")