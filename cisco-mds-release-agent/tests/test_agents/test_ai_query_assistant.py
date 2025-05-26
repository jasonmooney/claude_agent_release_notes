import unittest
from src.agents.ai_query_assistant import AIQueryAssistant

class TestAIQueryAssistant(unittest.TestCase):

    def setUp(self):
        self.aqa = AIQueryAssistant()

    def test_initialization(self):
        self.assertIsNotNone(self.aqa)

    def test_query_upgrade_path(self):
        response = self.aqa.query_upgrade_path("8.4(2)", "9.4(3a)")
        self.assertIn("upgrade path", response)

    def test_query_downgrade_path(self):
        response = self.aqa.query_downgrade_path("9.4(3a)", "8.4(2)")
        self.assertIn("downgrade path", response)

    def test_query_recommended_release(self):
        response = self.aqa.query_recommended_release("MDS 9700")
        self.assertIn("recommended release", response)

    def test_query_resolved_bugs(self):
        response = self.aqa.query_resolved_bugs("9.4(3a)")
        self.assertIn("resolved bugs", response)

if __name__ == '__main__':
    unittest.main()