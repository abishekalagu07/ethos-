from typing import List
from .models import (
    DeliveryInput, ContextAnalysis, RiskProfile, EthicalScore, 
    DeliveryDecision, DomainCategory
)
from .knowledge_base import (
    DOMAIN_KEYWORDS, RISK_BASE_SCORES, WEIGHTS, PRIORITY_THRESHOLDS
)
from .llm_client import LLMClient


class ContextLogic:
    @staticmethod
    def analyze(input_data: DeliveryInput) -> ContextAnalysis:
        desc = input_data.package_description.lower()
        detected_keywords = []
        domain = DomainCategory.GENERAL
        
        # Check specific domains in priority order
        # Medical > Emergency > Essential > General
        for d in [DomainCategory.MEDICAL, DomainCategory.EMERGENCY, DomainCategory.ESSENTIAL]:
            keywords = DOMAIN_KEYWORDS.get(d, [])
            found = [k for k in keywords if k in desc]
            if found:
                domain = d
                detected_keywords = found
                break # Stop at highest priority match for this simple version
        
        # 2. LLM Fallback (Hybrid Neuro-Symbolic)
        if domain == DomainCategory.GENERAL and not detected_keywords:
            # If no keywords found, try the LLM
            llm = LLMClient()
            llm_result = llm.classify_domain(desc)
            if llm_result and llm_result != DomainCategory.GENERAL:
                domain = llm_result
                detected_keywords = ["(LLM Classified)"]  # Marker that it was LLM

        
        # In this logic, Medical/Emergency implies human dependency
        is_dependent = domain in [DomainCategory.MEDICAL, DomainCategory.EMERGENCY]
        
        return ContextAnalysis(
            domain=domain,
            detected_keywords=detected_keywords,
            is_human_dependent=is_dependent
        )

# Move Imports to top or keep local if avoiding circular issues, but better at top.
# For this edit, we will import inside the method or rely on an updated import block.
# Let's update the import block first to be clean.


class RiskLogic:
    @staticmethod
    def estimate(context: ContextAnalysis) -> RiskProfile:
        # Look up base scores from Knowledge Base
        h, v, t = RISK_BASE_SCORES.get(context.domain, (1, 1, 1))
        
        # Dynamic adjustments could go here (e.g. if specific keywords increase urgency)
        # For now, we use the deterministic base mapping
        
        return RiskProfile(
            harm_severity=h,
            vulnerability=v,
            time_sensitivity=t
        )

class EthicalScoringEngine:
    @staticmethod
    def calculate(risk: RiskProfile) -> EthicalScore:
        w_h = WEIGHTS["HARM"]
        w_v = WEIGHTS["VULNERABILITY"]
        w_t = WEIGHTS["TIME"]
        
        score_h = risk.harm_severity * w_h
        score_v = risk.vulnerability * w_v
        score_t = risk.time_sensitivity * w_t
        
        total = score_h + score_v + score_t
        
        return EthicalScore(
            harm_score=score_h,
            vulnerability_score=score_v,
            time_score=score_t,
            total_score=round(total, 2)
        )

class DecisionLogic:
    @staticmethod
    def decide(score: EthicalScore, context: ContextAnalysis, risk: RiskProfile) -> DeliveryDecision:
        p1_thresh = PRIORITY_THRESHOLDS["P1"]
        p2_thresh = PRIORITY_THRESHOLDS["P2"]
        
        priority = 3 # Normal
        approval = False
        
        if score.total_score >= p1_thresh:
            priority = 1
            approval = True # Critical loads require oversight
        elif score.total_score >= p2_thresh:
            priority = 2
            
        # Explanation generation will happen in a separate module, but we pass placeholders here
        # or we invoke it here. To keep separation of concerns, we'll let the pipeline handle text generation
        # or we can pass a raw decision and let the explanation engine decorate it.
        # But `DeliveryDecision` needs an `explanation` field. We will leave it empty for the Pipeline to fill 
        # or simpler: we return the structure and the pipeline populates the text.
        # Let's return dummy text here or handle it in the next step. 
        # Re-reading plan: "Explanation Generation Logic... Output Natural-language justification"
        # We will create the decision object here.
        
        return DeliveryDecision(
            priority_level=priority,
            requires_approval=approval,
            explanation="", # To be filled by XAI module
            context=context,
            risk=risk,
            score=score
        )
