import unittest
from src.parsers.nx_os_parser import NXOSParser

class TestNXOSParser(unittest.TestCase):

    def setUp(self):
        self.parser = NXOSParser()

    def test_parse_release_notes(self):
        # Sample HTML content for testing
        sample_html = """
        <html>
            <body>
                <h1>Release Notes for NX-OS 9.4(3a)</h1>
                <p>First Published: 2025-05-25</p>
                <h2>Upgrade Paths</h2>
                <table>
                    <tr>
                        <th>Source Version</th>
                        <th>Upgrade Steps</th>
                    </tr>
                    <tr>
                        <td>Any 8.x prior to 8.4(2c)</td>
                        <td>Step 1: Upgrade to 8.4(2c), Step 2: Upgrade to 9.4(3a)</td>
                    </tr>
                </table>
            </body>
        </html>
        """
        expected_output = {
            "version": "9.4(3a)",
            "initial_release_date": "2025-05-25",
            "upgrade_paths": [
                {
                    "source_range_description": "Any 8.x prior to 8.4(2c)",
                    "steps": ["8.4(2c)", "9.4(3a)"]
                }
            ]
        }
        result = self.parser.parse_release_notes(sample_html)
        self.assertEqual(result, expected_output)

    def test_invalid_html(self):
        invalid_html = "<html><body><h1>No Release Info</h1></body></html>"
        with self.assertRaises(ValueError):
            self.parser.parse_release_notes(invalid_html)

if __name__ == '__main__':
    unittest.main()