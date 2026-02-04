from .models import DeliveryInput, DeliveryDecision
from .logic import ContextLogic, RiskLogic, EthicalScoringEngine, DecisionLogic
from .explanation import ExplanationEngine

class EthosPipeline:
    def process(self, package_desc: str, pickup: str = "N/A", dropoff: str = "N/A") -> DeliveryDecision:
        # 1. Create Input Model
        data = DeliveryInput(
            package_description=package_desc, 
            pickup_location=pickup, 
            delivery_location=dropoff
        )
        
        # 2. Pipeline Execution
        context = ContextLogic.analyze(data)
        risk = RiskLogic.estimate(context)
        score = EthicalScoringEngine.calculate(risk)
        decision = DecisionLogic.decide(score, context, risk)
        
        # 3. Add Explanation
        decision.explanation = ExplanationEngine.generate(decision)
        
        return decision
