from unittest import TestCase
from src.agents.data_consolidation_agent import DataConsolidationAgent

class TestDataConsolidationAgent(TestCase):
    def setUp(self):
        self.agent = DataConsolidationAgent()

    def test_initialization(self):
        self.assertIsNotNone(self.agent)
        self.assertIsInstance(self.agent, DataConsolidationAgent)

    def test_fetch_release_notes(self):
        # Assuming fetch_release_notes is a method in DataConsolidationAgent
        result = self.agent.fetch_release_notes()
        self.assertIsInstance(result, list)  # Assuming it returns a list of notes

    def test_parse_release_notes(self):
        # Assuming parse_release_notes is a method in DataConsolidationAgent
        sample_note = "<html>Sample Release Note</html>"
        parsed_data = self.agent.parse_release_notes(sample_note)
        self.assertIn('version', parsed_data)  # Check if version is extracted
        self.assertIn('release_date', parsed_data)  # Check if release date is extracted

    def test_store_data(self):
        # Assuming store_data is a method in DataConsolidationAgent
        sample_data = {'version': '9.4(3a)', 'release_date': '2025-05-25'}
        self.agent.store_data(sample_data)
        # Check if data is stored correctly (this will depend on your implementation)

    def tearDown(self):
        # Clean up if necessary
        pass