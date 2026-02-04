from .models import DeliveryDecision, ContextAnalysis, RiskProfile, EthicalScore

class ExplanationEngine:
    @staticmethod
    def generate(decision: DeliveryDecision) -> str:
        ctx = decision.context
        risk = decision.risk
        score = decision.score
        
        # 1. Context Statement
        if ctx.detected_keywords:
            context_str = f"Package contained keywords ({', '.join(ctx.detected_keywords)}) associated with the {ctx.domain.value} domain."
        else:
            context_str = f"Package classified as {ctx.domain.value} goods."

        # 2. Risk Factors
        risk_str = (
            f"Risk Profile assessed as:\n"
            f"  - Harm Potential: {risk.harm_severity}/10 (Weight: {score.harm_score:.1f})\n"
            f"  - Vulnerability: {risk.vulnerability}/10 (Weight: {score.vulnerability_score:.1f})\n"
            f"  - Time Sensitivity: {risk.time_sensitivity}/10 (Weight: {score.time_score:.1f})"
        )

        # 3. Decision Rationale
        if decision.priority_level == 1:
            rationale = "CRITICAL PRIORITY assigned due to high ethical risk score indicating potential severe harm or vulnerability."
        elif decision.priority_level == 2:
            rationale = "HIGH PRIORITY assigned based on elevated importance compared to general goods."
        else:
            rationale = "STANDARD PRIORITY assigned. No immediate ethical risks detected."
            
        final_text = (
            f"DECISION EXPLANATION:\n"
            f"{context_str}\n"
            f"{risk_str}\n"
            f"Total Ethical Score: {score.total_score:.2f}\n"
            f"CONCLUSION: {rationale}"
        )
        
        if decision.requires_approval:
            final_text += "\n[SAFETY INTERVENTION]: Human approval required for Priority 1 dispatch."
            
        return final_text
