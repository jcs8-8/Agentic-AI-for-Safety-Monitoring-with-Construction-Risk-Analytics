from enum import Enum

class RiskType(str, Enum):
    FALL_HAZARD = "fall_hazard"
    EQUIPMENT_RISK = "equipment_risk"
    ELECTRICAL_HAZARD = "electrical_hazard"
    ENVIRONMENTAL_RISK = "environmental_risk"
    STRUCTURAL_RISK = "structural_risk"

class Severity(int, Enum):
    NEGLIGIBLE = 1
    MINOR = 2
    MODERATE = 3
    MAJOR = 4
    CATASTROPHIC = 5
