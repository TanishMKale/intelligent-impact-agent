-- LOB
INSERT INTO lob (lob_id, lob_name) VALUES
('LOB-PAY', 'Payments'),
('LOB-CBS', 'Core Banking'),
('LOB-CRM', 'Customer Management');

-- APPLICATIONS
INSERT INTO application (application_id, lob_id, name, criticality) VALUES
('APP-PAY', 'LOB-PAY', 'Payment Hub', 'Critical'),
('APP-CBS', 'LOB-CBS', 'Core Banking System', 'Critical'),
('APP-CRM', 'LOB-CRM', 'CRM', 'High');

-- MODULES
INSERT INTO module (module_id, application_id, name, criticality) VALUES
('MOD-PAY-ONB', 'APP-PAY', 'Customer Onboarding', 'Critical'),
('MOD-PAY-BEN', 'APP-PAY', 'Beneficiary Management', 'High'),
('MOD-CBS-CIF', 'APP-CBS', 'CIF / Customer Master', 'Critical'),
('MOD-CBS-ACC', 'APP-CBS', 'Account Services', 'Critical'),
('MOD-CRM-PROF', 'APP-CRM', 'Customer Profile', 'High'),
('MOD-CRM-COMM', 'APP-CRM', 'Communication Preferences', 'Medium');

-- DEPENDENCIES (directed: source -> target)
INSERT INTO application_dependency
(dependency_id, source_module_id, target_module_id, relationship_type, description, criticality) VALUES
('DEP-001', 'MOD-PAY-ONB', 'MOD-CBS-CIF', 'CUSTOMER_VALIDATION', 'Payments validates customer/CIF data in CBS.', 'Critical'),
('DEP-002', 'MOD-PAY-ONB', 'MOD-CRM-PROF', 'PROFILE_SYNC', 'Successful onboarding updates customer profile.', 'High'),
('DEP-003', 'MOD-CBS-CIF', 'MOD-CRM-PROF', 'CUSTOMER_MASTER_SYNC', 'Customer master changes can propagate to CRM.', 'High'),
('DEP-004', 'MOD-PAY-BEN', 'MOD-CBS-ACC', 'ACCOUNT_VALIDATION', 'Beneficiary flow validates account status/details.', 'Critical');

-- REQUIREMENTS
INSERT INTO requirement
(requirement_id, project, release, application_id, module_id, description, status) VALUES
('REQ-PAY-001', 'POC-Bank', 'R1', 'APP-PAY', 'MOD-PAY-ONB', 'Validate customer identity before payment profile activation.', 'ACTIVE'),
('REQ-PAY-002', 'POC-Bank', 'R1', 'APP-PAY', 'MOD-PAY-ONB', 'Customer onboarding must use registered mobile number.', 'ACTIVE'),
('REQ-PAY-003', 'POC-Bank', 'R1', 'APP-PAY', 'MOD-PAY-ONB', 'Successful onboarding must update customer profile.', 'ACTIVE'),
('REQ-CBS-001', 'POC-Bank', 'R1', 'APP-CBS', 'MOD-CBS-CIF', 'Expose active customer/CIF status for consuming channels.', 'ACTIVE'),
('REQ-CBS-002', 'POC-Bank', 'R1', 'APP-CBS', 'MOD-CBS-CIF', 'Return registered mobile number for customer validation.', 'ACTIVE'),
('REQ-CBS-003', 'POC-Bank', 'R1', 'APP-CBS', 'MOD-CBS-ACC', 'Expose account status for downstream validation.', 'ACTIVE'),
('REQ-CRM-001', 'POC-Bank', 'R1', 'APP-CRM', 'MOD-CRM-PROF', 'Maintain synchronized customer contact and onboarding status.', 'ACTIVE'),
('REQ-CRM-002', 'POC-Bank', 'R1', 'APP-CRM', 'MOD-CRM-COMM', 'Use registered communication preferences for notifications.', 'ACTIVE');

-- TEST CASES
INSERT INTO test_case
(test_case_id, application_id, module_id, scenario, description, steps, expected_result, precondition, test_data, test_mode, category) VALUES
('TC-PAY-001', 'APP-PAY', 'MOD-PAY-ONB',
 'Verify valid existing customer can complete onboarding after identity validation.',
 'Existing customer onboarding with successful identity validation against core banking.',
 '1. Enter valid CIF. 2. Submit onboarding. 3. Complete identity validation.',
 'Onboarding completes and payment profile is activated.',
 'Customer exists in CBS with active status.',
 'CIF: 100001', 'Manual', 'Functional'),
('TC-PAY-002', 'APP-PAY', 'MOD-PAY-ONB',
 'Verify onboarding is blocked when customer validation fails.',
 'Negative test where customer validation fails and onboarding must stop.',
 '1. Enter invalid or unknown CIF. 2. Submit onboarding.',
 'Onboarding is blocked with a validation error.',
 'Customer validation service is available.',
 'CIF: 999999', 'Manual', 'Negative'),
('TC-PAY-003', 'APP-PAY', 'MOD-PAY-ONB',
 'Verify OTP/onboarding uses registered customer mobile number.',
 'OTP is sent only to the mobile number registered for the customer.',
 '1. Start onboarding. 2. Request OTP.',
 'OTP is sent to the registered mobile number only.',
 'Customer has a registered mobile number.',
 'Mobile: 9876543210', 'Manual', 'Functional'),
('TC-PAY-004', 'APP-PAY', 'MOD-PAY-ONB',
 'Verify customer profile is updated after successful onboarding.',
 'After onboarding succeeds, customer profile is updated with onboarding status.',
 '1. Complete onboarding. 2. Check customer profile.',
 'Customer profile shows onboarding status as completed.',
 'Onboarding completed successfully.',
 'CIF: 100001', 'Manual', 'Integration'),
('TC-CBS-001', 'APP-CBS', 'MOD-CBS-CIF',
 'Verify CIF service returns active customer status.',
 'CIF service returns active status for an active customer.',
 '1. Call CIF status service with valid CIF.',
 'Response shows customer status as ACTIVE.',
 'Active customer exists in CIF.',
 'CIF: 100001', 'Manual', 'Functional'),
('TC-CBS-002', 'APP-CBS', 'MOD-CBS-CIF',
 'Verify CIF service returns registered mobile number.',
 'CIF service returns the registered mobile number for customer validation.',
 '1. Call CIF customer service with valid CIF.',
 'Response contains the registered mobile number.',
 'Customer has a registered mobile number.',
 'CIF: 100001', 'Manual', 'Functional'),
('TC-CBS-003', 'APP-CBS', 'MOD-CBS-CIF',
 'Verify inactive CIF is rejected by consuming channel.',
 'Consuming channel must reject a customer whose CIF status is inactive.',
 '1. Use inactive CIF in consuming channel. 2. Submit request.',
 'Request is rejected because customer CIF is inactive.',
 'CIF exists with status INACTIVE.',
 'CIF: 100002 (inactive)', 'Manual', 'Negative'),
('TC-CBS-004', 'APP-CBS', 'MOD-CBS-ACC',
 'Verify active account status response for beneficiary validation.',
 'Account services returns active account status for beneficiary validation.',
 '1. Call account status service with valid account number.',
 'Response shows account status as ACTIVE.',
 'Active account exists.',
 'Account: 5000100', 'Manual', 'Functional'),
('TC-CRM-001', 'APP-CRM', 'MOD-CRM-PROF',
 'Verify customer onboarding status synchronizes to CRM.',
 'Onboarding status from Payments is synchronized into the CRM customer profile.',
 '1. Complete onboarding in Payments. 2. Open customer in CRM.',
 'CRM profile shows updated onboarding status.',
 'Onboarding completed in Payments.',
 'CIF: 100001', 'Manual', 'Integration'),
('TC-CRM-002', 'APP-CRM', 'MOD-CRM-PROF',
 'Verify customer contact number synchronization after profile update.',
 'Customer contact number is kept in sync in CRM after the profile is updated.',
 '1. Update customer profile contact number. 2. Check CRM contact details.',
 'CRM shows the latest synchronized contact number.',
 'Customer profile exists in CRM.',
 'Mobile: 9123456780', 'Manual', 'Integration'),
('TC-CRM-003', 'APP-CRM', 'MOD-CRM-COMM',
 'Verify marketing communication preference update.',
 'Customer updates marketing communication preference in CRM.',
 '1. Open communication preferences. 2. Change marketing preference. 3. Save.',
 'Marketing preference is saved.',
 'Customer exists in CRM.',
 'Preference: Email OFF', 'Manual', 'Functional'),
('TC-PAY-005', 'APP-PAY', 'MOD-PAY-BEN',
 'Verify beneficiary account validation for active account.',
 'Beneficiary can be added when the destination account is active.',
 '1. Enter beneficiary account number. 2. Submit.',
 'Beneficiary is added after account validation.',
 'Destination account is active.',
 'Account: 5000100', 'Manual', 'Functional');

-- TRACEABILITY
INSERT INTO requirement_testcase_map (requirement_id, test_case_id) VALUES
('REQ-PAY-001', 'TC-PAY-001'),
('REQ-PAY-001', 'TC-PAY-002'),
('REQ-PAY-002', 'TC-PAY-003'),
('REQ-PAY-003', 'TC-PAY-004'),
('REQ-CBS-001', 'TC-CBS-001'),
('REQ-CBS-002', 'TC-CBS-002'),
('REQ-CBS-003', 'TC-CBS-004'),
('REQ-CRM-001', 'TC-CRM-001'),
('REQ-CRM-002', 'TC-CRM-003');