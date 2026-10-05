from app.services.dependency_service import get_impacted_modules

tests = [
    ("MOD-PAY-ONB", "CR-001 Payments Onboarding"),
    ("MOD-PAY-BEN", "CR-002 Payments Beneficiary"),
    ("MOD-CRM-COMM", "CR-003 CRM Comm Preferences"),
]

for module_id, label in tests:
    print("=" * 60)
    print(label, "->", module_id)
    impacted = get_impacted_modules(module_id, depth=2)

    if not impacted:
        print("  (no impacted modules)")

    for item in impacted:
        print(f"  depth {item['depth']}: {item['application_name']} / {item['module_name']}")
        print(f"           relationship: {item['relationship_type']}")
        print(f"           path: {' -> '.join(item['path'])}")