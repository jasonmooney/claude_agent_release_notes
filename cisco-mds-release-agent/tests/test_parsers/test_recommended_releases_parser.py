import unittest
from src.parsers.recommended_releases_parser import RecommendedReleasesParser

class TestRecommendedReleasesParser(unittest.TestCase):

    def setUp(self):
        self.parser = RecommendedReleasesParser()

    def test_parse_recommended_releases(self):
        # Assuming we have a method to test the parsing of recommended releases
        result = self.parser.parse_recommended_releases()
        self.assertIsInstance(result, dict)  # Check if the result is a dictionary
        self.assertIn('open_systems', result)  # Check if 'open_systems' key exists
        self.assertIn('ficon', result)  # Check if 'ficon' key exists

    def test_parse_recommendation_dates(self):
        # Test the extraction of recommendation dates
        result = self.parser.parse_recommended_releases()
        for platform in ['open_systems', 'ficon']:
            for recommendation in result[platform]:
                self.assertIn('recommended_since', recommendation)  # Check if recommendation date exists

if __name__ == '__main__':
    unittest.main()