from .models import DomainCategory

# 1. KEYWORD KNOWLEDGE BASE
# Maps keywords to domains
DOMAIN_KEYWORDS = {
    DomainCategory.MEDICAL: [
        "medicine", "insulin", "blood", "organ", "vaccine", "pharmacy", "doctor", 
        "hospital", "prescription", "heart", "kidney", "monitor", "oxygen"
    ],
    DomainCategory.EMERGENCY: [
        "disaster", "flood", "fire", "rescue", "relief", "urgency", "critical", 
        "collapsed", "search", "evacuation"
    ],
    DomainCategory.ESSENTIAL: [
        "food", "water", "grocery", "baby", "diaper", "sanitary", "heating", 
        "repair", "plumbing"
    ]
}

# 2. RISK MAPPING RULES
# Base scores (0-10) for each domain if no specific overrides apply
# Format: (Harm, Vulnerability, TimeSensitivity)
RISK_BASE_SCORES = {
    DomainCategory.MEDICAL:   (9, 9, 8),
    DomainCategory.EMERGENCY: (8, 9, 9),
    DomainCategory.ESSENTIAL: (4, 5, 4),
    DomainCategory.GENERAL:   (1, 1, 1)
}

# 3. ETHICAL WEIGHTS (Configurable)
# Adjust these to change system behavior based on values
WEIGHTS = {
    "HARM": 0.4,           # Weight for Harm Severity (w1)
    "VULNERABILITY": 0.35, # Weight for Vulnerability (w2)
    "TIME": 0.25           # Weight for Time Sensitivity (w3)
}

# 4. DECISION THRESHOLDS
PRIORITY_THRESHOLDS = {
    "P1": 8.0,  # Critical
    "P2": 6.0   # High
}
