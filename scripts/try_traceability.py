from app.services.dependency_service import get_impacted_modules
from app.services.traceability_service import (
    get_requirements_for_modules,
    get_mapped_test_cases,
)

tests = [
    ("MOD-PAY-ONB", "CR-001 Payments Onboarding"),
    ("MOD-PAY-BEN", "CR-002 Payments Beneficiary"),
    ("MOD-CRM-COMM", "CR-003 CRM Comm Preferences"),
]

for source_module, label in tests:
    print("=" * 60)
    print(label)

    # Step 3: which modules are impacted?
    impacted = get_impacted_modules(source_module, depth=2)

    # source module + impacted modules
    all_module_ids = [source_module]
    for item in impacted:
        all_module_ids.append(item["module_id"])
    print("Modules:", all_module_ids)

    # Step 4a: requirements in those modules
    requirements = get_requirements_for_modules(all_module_ids)
    print("Requirements:")
    for req in requirements:
        print("  ", req["requirement_id"], "-", req["description"])

    # Step 4b: test cases mapped to those requirements
    req_ids = [req["requirement_id"] for req in requirements]
    test_cases = get_mapped_test_cases(req_ids)
    print("Mapped test cases:")
    for tc in test_cases:
        print("  ", tc["test_case_id"], "(via", tc["mapped_requirement_id"] + ")")