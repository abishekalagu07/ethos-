from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

class UrgencyLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class DomainCategory(str, Enum):
    MEDICAL = "MEDICAL"
    EMERGENCY = "EMERGENCY"
    ESSENTIAL = "ESSENTIAL"
    GENERAL = "GENERAL"

@dataclass
class DeliveryInput:
    package_description: str
    pickup_location: str
    delivery_location: str

@dataclass
class ContextAnalysis:
    domain: DomainCategory
    detected_keywords: List[str]
    is_human_dependent: bool

@dataclass
class RiskProfile:
    harm_severity: int      # 0-10
    vulnerability: int      # 0-10
    time_sensitivity: int   # 0-10

@dataclass
class EthicalScore:
    harm_score: float
    vulnerability_score: float
    time_score: float
    total_score: float

@dataclass
class DeliveryDecision:
    priority_level: int     # 1 (Critical), 2 (High), 3 (Normal)
    requires_approval: bool
    explanation: str
    context: ContextAnalysis
    risk: RiskProfile
    score: EthicalScore
