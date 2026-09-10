-- Seed data for BuildSure AI
INSERT INTO projects (project_id, project_name, location, start_date, status) VALUES
('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Downtown High-Rise Tower', '123 Main St, Downtown', '2026-01-15', 'active'),
('b2c3d4e5-f6a7-8901-bcde-f12345678901', 'Highway Bridge Extension', 'I-95 Mile Marker 42', '2026-03-01', 'active'),
('c3d4e5f6-a7b8-9012-cdef-123456789012', 'Industrial Warehouse Complex', 'Zone 7 Industrial Park', '2025-11-20', 'active');

INSERT INTO site_risks (risk_id, project_id, risk_type, severity, probability, impact, detected_at, location_zone, description, mitigation_status, ai_confidence) VALUES
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'fall_hazard', 4, 4, 4, NOW() - INTERVAL '2 days', 'Zone A', 'Unsecured scaffolding on floor 12', 'open', 0.92),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'fall_hazard', 5, 3, 5, NOW() - INTERVAL '1 day', 'Zone B', 'Open edge protection missing on floor 15', 'open', 0.95),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'equipment_risk', 3, 4, 3, NOW() - INTERVAL '3 days', 'Zone C', 'Crane load exceeding rated capacity', 'mitigated', 0.88),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'equipment_risk', 4, 3, 4, NOW() - INTERVAL '5 days', 'Zone D', 'Concrete mixer hydraulic leak detected', 'open', 0.85),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'electrical_hazard', 3, 3, 3, NOW() - INTERVAL '1 day', 'Zone A', 'Exposed wiring near wet area', 'open', 0.90),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'electrical_hazard', 4, 2, 4, NOW() - INTERVAL '4 days', 'Zone E', 'Temporary power distribution panel overload', 'mitigated', 0.87),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'environmental_risk', 2, 3, 2, NOW() - INTERVAL '6 days', 'Zone B', 'Dust suppression system malfunction', 'open', 0.78),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'environmental_risk', 3, 2, 3, NOW() - INTERVAL '7 days', 'Zone C', 'Stormwater runoff containment breach', 'accepted', 0.82),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'structural_risk', 4, 3, 4, NOW() - INTERVAL '2 days', 'Zone D', 'Foundation settlement monitoring alert', 'open', 0.91),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'fall_hazard', 3, 4, 3, NOW() - INTERVAL '8 days', 'Zone E', 'Ladder not secured at base', 'mitigated', 0.86),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'equipment_risk', 3, 3, 3, NOW() - INTERVAL '9 days', 'Zone A', 'Excavator track wear beyond tolerance', 'open', 0.84),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'electrical_hazard', 2, 2, 2, NOW() - INTERVAL '10 days', 'Zone B', 'Extension cord damage on ground floor', 'mitigated', 0.80);

INSERT INTO site_risks (risk_id, project_id, risk_type, severity, probability, impact, detected_at, location_zone, description, mitigation_status, ai_confidence)
SELECT gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
  (ARRAY['fall_hazard', 'equipment_risk', 'electrical_hazard', 'environmental_risk', 'structural_risk'])[1 + (i % 5)],
  2 + (i % 4), 2 + (i % 4), 2 + (i % 4),
  NOW() - INTERVAL '1 day' * i,
  (ARRAY['Zone A', 'Zone B', 'Zone C', 'Zone D', 'Zone E'])[1 + (i % 5)],
  'Auto-generated risk ' || i, 'open', 0.75 + (i % 20) / 100.0
FROM generate_series(1, 35) AS i;

INSERT INTO safety_incidents (incident_id, project_id, incident_type, severity, incident_date, worker_id, worker_name, description, location_zone, ppe_involved, status) VALUES
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'near_miss', 2, NOW() - INTERVAL '1 day', 'W001', 'John Smith', 'Worker nearly struck by falling debris', 'Zone A', false, 'closed'),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'injury', 3, NOW() - INTERVAL '3 days', 'W002', 'Mike Johnson', 'Minor cut from sharp metal edge', 'Zone B', false, 'open'),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'near_miss', 2, NOW() - INTERVAL '5 days', 'W003', 'Sarah Williams', 'Slip on wet surface near equipment', 'Zone C', false, 'closed'),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'equipment_damage', 4, NOW() - INTERVAL '7 days', 'W004', 'David Brown', 'Concrete pump hose rupture', 'Zone D', false, 'investigating');

INSERT INTO ppe_violations (violation_id, project_id, worker_id, worker_name, violation_type, timestamp, location_zone, ai_confidence, resolved) VALUES
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'W001', 'John Smith', 'missing_hard_hat', NOW() - INTERVAL '2 hours', 'Zone A', 0.92, false),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'W005', 'Robert Lee', 'no_safety_vest', NOW() - INTERVAL '4 hours', 'Zone B', 0.94, false),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'W010', 'Lisa Chen', 'no_protective_gloves', NOW() - INTERVAL '1 day', 'Zone C', 0.89, true),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'W015', 'Tom Wilson', 'no_safety_boots', NOW() - INTERVAL '2 days', 'Zone D', 0.91, false),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'W020', 'Amy Zhang', 'missing_hard_hat', NOW() - INTERVAL '3 days', 'Zone E', 0.96, true);

INSERT INTO compliance_checks (compliance_id, project_id, regulation_name, regulation_category, compliance_status, checked_at, severity) VALUES
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'OSHA-1926.501', 'OSHA_Standards', 'compliant', NOW() - INTERVAL '1 day', 1),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'OSHA-1926.453', 'OSHA_Standards', 'compliant', NOW() - INTERVAL '2 days', 1),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'IBC-2021-Section-1705', 'Building_Codes', 'compliant', NOW() - INTERVAL '3 days', 2),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Local-Zoning-Ordinance-42', 'Building_Codes', 'pending', NOW() - INTERVAL '1 day', 2),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'EPA-Clean-Air-Act', 'Environmental_Regulations', 'compliant', NOW() - INTERVAL '5 days', 1),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'EPA-Stormwater-Permit', 'Environmental_Regulations', 'violation', NOW() - INTERVAL '2 days', 3),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'GL-Policy-2026', 'Insurance_Requirements', 'compliant', NOW() - INTERVAL '7 days', 1),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Workers-Comp-Coverage', 'Insurance_Requirements', 'compliant', NOW() - INTERVAL '8 days', 1);

INSERT INTO insurance_cases (case_id, project_id, claim_type, risk_score, risk_level, status, estimated_liability, incident_date, description) VALUES
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'workers_comp', 45.0, 'Medium', 'open', 125000.00, NOW() - INTERVAL '10 days', 'Potential workers comp claim from slip incident'),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'property_damage', 35.0, 'Medium', 'open', 75000.00, NOW() - INTERVAL '15 days', 'Equipment damage from hydraulic failure'),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'liability', 55.0, 'Medium', 'under_review', 250000.00, NOW() - INTERVAL '20 days', 'Third-party liability from falling debris'),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'environmental', 25.0, 'Low', 'closed', 50000.00, NOW() - INTERVAL '30 days', 'Environmental cleanup from minor spill');

INSERT INTO alerts (alert_id, project_id, alert_type, severity, severity_label, message, created_at, acknowledged, source_agent) VALUES
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'site_risk', 4, 'High', 'High-risk fall hazard detected in Zone B - Open edge protection missing', NOW() - INTERVAL '1 hour', false, 'SiteRiskAgent'),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'safety_violation', 3, 'Medium', 'PPE violation: Missing hard hat detected for Worker W001', NOW() - INTERVAL '2 hours', false, 'SafetyAgent'),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'compliance_violation', 3, 'Medium', 'EPA Stormwater Permit violation detected', NOW() - INTERVAL '1 day', false, 'ComplianceAgent'),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'insurance_alert', 3, 'Medium', 'Liability case risk score increased to 55', NOW() - INTERVAL '2 days', false, 'InsuranceAgent');

INSERT INTO reports (report_id, project_id, report_type, generated_at, file_format, content_summary, generated_by) VALUES
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'daily_site', NOW() - INTERVAL '1 day', 'pdf', 'Daily site operations summary with 12 risks identified', 'Reporting Agent'),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'executive_summary', NOW() - INTERVAL '3 days', 'pdf', 'Executive risk overview for board review', 'Reporting Agent'),
(gen_random_uuid(), 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'safety_analysis', NOW() - INTERVAL '5 days', 'excel', 'Detailed safety incident analysis Q3 2026', 'Reporting Agent');

INSERT INTO users (user_id, email, hashed_password, full_name, role, is_active) VALUES
('d4e5f6a7-b8c9-0123-defa-234567890123', 'admin@buildsure.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYA.qGZvKG6G', 'Admin User', 'admin', true),
('e5f6a7b8-c9d0-1234-efab-345678901234', 'manager@buildsure.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYA.qGZvKG6G', 'John Doe', 'site_manager', true);
