import unittest
from src.pipeline import EthosPipeline
from src.models import DomainCategory

class TestEthosScenarios(unittest.TestCase):
    def setUp(self):
        self.pipeline = EthosPipeline()
    
    def test_medical_critical(self):
        # Scenario: Insulin delivery
        desc = "Urgent delivery of insulin for a diabetic patient"
        decision = self.pipeline.process(desc)
        
        self.assertEqual(decision.context.domain, DomainCategory.MEDICAL)
        self.assertEqual(decision.priority_level, 1)
        self.assertTrue(decision.requires_approval)
        print(f"\n[PASS] Medical Scenario: {desc} -> P{decision.priority_level}")

    def test_emergency_rescue(self):
        # Scenario: Flood relief
        desc = "Rescue equipment for flood victims"
        decision = self.pipeline.process(desc)
        
        self.assertEqual(decision.context.domain, DomainCategory.EMERGENCY)
        self.assertEqual(decision.priority_level, 1)
        print(f"\n[PASS] Emergency Scenario: {desc} -> P{decision.priority_level}")

    def test_general_goods(self):
        # Scenario: Gaming console
        desc = "PlayStation 5 console"
        decision = self.pipeline.process(desc)
        
        self.assertEqual(decision.context.domain, DomainCategory.GENERAL)
        self.assertEqual(decision.priority_level, 3)
        self.assertFalse(decision.requires_approval)
        print(f"\n[PASS] General Scenario: {desc} -> P{decision.priority_level}")

    def test_educational_essential(self):
        # Scenario: School text books - might be General or Essential depending on keywords
        # Our KW list: Essential = food, water, etc. Books -> General
        desc = "Box of school textbooks"
        decision = self.pipeline.process(desc)
        
        self.assertEqual(decision.context.domain, DomainCategory.GENERAL) 
        # Note: If we want books to be essential, we'd add 'textbook' to ESSENTIAL keywords.
        # Based on current rule: General.
        self.assertEqual(decision.priority_level, 3)
        print(f"\n[PASS] Educational Scenario: {desc} -> P{decision.priority_level}")

if __name__ == '__main__':
    unittest.main()
