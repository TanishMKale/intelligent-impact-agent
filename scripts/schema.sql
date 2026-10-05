CREATE TABLE lob (
    lob_id TEXT PRIMARY KEY,
    lob_name TEXT NOT NULL
);

CREATE TABLE application (
    application_id TEXT PRIMARY KEY,
    lob_id TEXT REFERENCES lob(lob_id),
    name TEXT NOT NULL,
    criticality TEXT NOT NULL
);

CREATE TABLE module (
    module_id TEXT PRIMARY KEY,
    application_id TEXT REFERENCES application(application_id),
    name TEXT NOT NULL,
    criticality TEXT NOT NULL
);

CREATE TABLE application_dependency (
    dependency_id TEXT PRIMARY KEY,
    source_module_id TEXT REFERENCES module(module_id),
    target_module_id TEXT REFERENCES module(module_id),
    relationship_type TEXT NOT NULL,
    description TEXT,
    criticality TEXT
);

CREATE TABLE requirement (
    requirement_id TEXT PRIMARY KEY,
    project TEXT,
    release TEXT,
    application_id TEXT REFERENCES application(application_id),
    module_id TEXT REFERENCES module(module_id),
    description TEXT NOT NULL,
    status TEXT DEFAULT 'ACTIVE'
);

CREATE TABLE test_case (
    test_case_id TEXT PRIMARY KEY,
    application_id TEXT REFERENCES application(application_id),
    module_id TEXT REFERENCES module(module_id),
    scenario TEXT NOT NULL,
    description TEXT,
    steps TEXT,
    expected_result TEXT,
    precondition TEXT,
    test_data TEXT,
    test_mode TEXT,
    category TEXT
);

CREATE TABLE requirement_testcase_map (
    requirement_id TEXT REFERENCES requirement(requirement_id),
    test_case_id TEXT REFERENCES test_case(test_case_id),
    PRIMARY KEY (requirement_id, test_case_id)
);

CREATE TABLE defect (
    defect_id TEXT PRIMARY KEY,
    test_case_id TEXT REFERENCES test_case(test_case_id),
    application_id TEXT,
    module_id TEXT,
    severity TEXT,
    priority TEXT,
    status TEXT,
    description TEXT
);

-- audit tables (used later)
CREATE TABLE impact_run (
    run_id TEXT PRIMARY KEY,
    cr_id TEXT,
    input_text TEXT,
    extracted_json JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    status TEXT
);

CREATE TABLE impact_result (
    id SERIAL PRIMARY KEY,
    run_id TEXT REFERENCES impact_run(run_id),
    entity_type TEXT,
    entity_id TEXT,
    evidence_type TEXT,
    score NUMERIC,
    reason TEXT,
    included BOOLEAN
);

CREATE TABLE review_action (
    id SERIAL PRIMARY KEY,
    run_id TEXT REFERENCES impact_run(run_id),
    reviewer TEXT,
    entity_id TEXT,
    action TEXT,
    reason TEXT,
    timestamp TIMESTAMP DEFAULT NOW()
);