import unittest
from src.parsers.epld_parser import EPLDParser

class TestEPLDParser(unittest.TestCase):

    def setUp(self):
        self.parser = EPLDParser()

    def test_parse_epld_release(self):
        # Sample EPLD release note content
        sample_content = """
        EPLD Release Notes
        Release Version: EPLD-2024.01.15
        Release Date: 2024-01-15
        Hardware Versions:
        - MDS 9710 Director: Supervisor PMFPGA version 1.2.3
        - MDS 9300: Supervisor PMFPGA version 1.2.4
        """
        expected_output = {
            'release_version': 'EPLD-2024.01.15',
            'release_date': '2024-01-15',
            'hardware_versions': [
                {'device': 'MDS 9710 Director', 'version': '1.2.3'},
                {'device': 'MDS 9300', 'version': '1.2.4'}
            ]
        }
        result = self.parser.parse(sample_content)
        self.assertEqual(result, expected_output)

    def test_invalid_epld_format(self):
        # Sample invalid EPLD release note content
        invalid_content = "This is not a valid EPLD release note."
        with self.assertRaises(ValueError):
            self.parser.parse(invalid_content)

if __name__ == '__main__':
    unittest.main()