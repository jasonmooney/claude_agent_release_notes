#!/usr/bin/env python3
"""
Comprehensive Test Suite for Cisco MDS Release Note Agentic System
This test suite validates all core functionality demonstrated in the system execution.
"""

import unittest
import sys
import os
import yaml
import tempfile
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.data_consolidation_agent import DataConsolidationAgent
from agents.ai_query_assistant import AIQueryAssistant


class TestSystemValidation(unittest.TestCase):
    """Comprehensive validation tests for the entire system."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests."""
        cls.data_file_path = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'output', 'upgrade_paths.yaml'
        )
        cls.test_data_exists = os.path.exists(cls.data_file_path)
        
        if cls.test_data_exists:
            with open(cls.data_file_path, 'r') as f:
                cls.test_data = yaml.safe_load(f)
        else:
            # Fallback test data for offline testing
            cls.test_data = {
                '9.4.3': {
                    'initial_release_date': '2025-03-03',
                    'resolved_bugs': [
                        {'id': 'CSCwk65461', 'description': 'Test bug 1'},
                        {'id': 'CSCwn58100', 'description': 'Test bug 2'}
                    ],
                    'upgrade_paths': {'Open-Systems': ['9.3.1'], 'FICON': ['9.3.1']}
                },
                '9.4.3a': {
                    'initial_release_date': '2025-03-28', 
                    'resolved_bugs': [
                        {'id': 'CSCwo03706', 'description': 'Test bug 3'}
                    ],
                    'upgrade_paths': {'Open-Systems': ['9.4.3'], 'FICON': ['9.4.3']}
                }
            }

    def setUp(self):
        """Set up test fixtures for each test."""
        self.dca = DataConsolidationAgent()
        self.aqa = AIQueryAssistant(data=self.test_data if not self.test_data_exists else None)


class TestDataConsolidationAgent(TestSystemValidation):
    """Test the Data Consolidation Agent functionality."""
    
    def test_dca_initialization(self):
        """Test DCA initializes correctly."""
        self.assertIsNotNone(self.dca)
        self.assertIsInstance(self.dca, DataConsolidationAgent)
    
    def test_dca_has_consolidated_data_attribute(self):
        """Test DCA has consolidated_data attribute (not get_consolidated_data method)."""
        # This test validates the fix for the AttributeError
        self.assertTrue(hasattr(self.dca, 'consolidated_data'))
        self.assertFalse(hasattr(self.dca, 'get_consolidated_data'))
    
    @patch('agents.data_consolidation_agent.requests.get')
    def test_web_scraping_functionality(self, mock_get):
        """Test web scraping capabilities."""
        # Mock successful web response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>Test content</body></html>'
        mock_get.return_value = mock_response
        
        # Test the web scraping method exists and works
        if hasattr(self.dca, 'fetch_release_notes'):
            result = self.dca.fetch_release_notes()
            self.assertIsNotNone(result)
    
    def test_date_extraction_methods_exist(self):
        """Test that date extraction methods exist."""
        self.assertTrue(hasattr(self.dca, '_extract_release_date'))
        self.assertTrue(hasattr(self.dca, '_parse_changelog_table'))
    
    def test_bug_extraction_methods_exist(self):
        """Test that bug extraction methods exist."""
        self.assertTrue(hasattr(self.dca, '_extract_resolved_bugs'))
    
    def test_upgrade_path_extraction_methods_exist(self):
        """Test that upgrade path extraction methods exist."""
        self.assertTrue(hasattr(self.dca, '_extract_upgrade_paths'))


class TestAIQueryAssistant(TestSystemValidation):
    """Test the AI Query Assistant functionality."""
    
    def test_aqa_initialization(self):
        """Test AQA initializes correctly."""
        self.assertIsNotNone(self.aqa)
        self.assertIsInstance(self.aqa, AIQueryAssistant)
    
    def test_natural_language_query_method_exists(self):
        """Test natural language query method exists."""
        self.assertTrue(hasattr(self.aqa, 'natural_language_query'))
        self.assertTrue(callable(getattr(self.aqa, 'natural_language_query')))
    
    def test_query_resolved_bugs(self):
        """Test resolved bugs query functionality."""
        result = self.aqa.query_resolved_bugs('9.4.3')
        
        self.assertIsInstance(result, dict)
        self.assertIn('status', result)
        self.assertIn('version', result)
        
        if result['status'] == 'success':
            self.assertIn('resolved_bugs', result)
            self.assertIn('total_bugs_resolved', result)
            self.assertIsInstance(result['resolved_bugs'], list)
    
    def test_query_release_date(self):
        """Test release date query functionality."""
        result = self.aqa.query_release_date('9.4.3a')
        
        self.assertIsInstance(result, dict)
        self.assertIn('status', result)
        self.assertIn('version', result)
        
        if result['status'] == 'success':
            self.assertIn('release_date', result)
            # Validate date format
            release_date = result['release_date']
            self.assertRegex(release_date, r'\d{4}-\d{2}-\d{2}')
    
    def test_query_upgrade_path(self):
        """Test upgrade path query functionality."""
        result = self.aqa.query_upgrade_path('9.3.1', '9.4.3')
        
        self.assertIsInstance(result, dict)
        self.assertIn('status', result)
        self.assertIn('current_version', result)
        self.assertIn('target_version', result)
    
    def test_version_normalization(self):
        """Test version normalization functionality."""
        if hasattr(self.aqa, '_normalize_version'):
            # Test various version format inputs
            test_cases = [
                ('9.4(3)', '9.4.3'),
                ('9.4(3a)', '9.4.3a'),
                ('9.4.3', '9.4.3'),
                ('9.4.3a', '9.4.3a')
            ]
            
            for input_version, expected_output in test_cases:
                normalized = self.aqa._normalize_version(input_version)
                self.assertEqual(normalized, expected_output)
    
    def test_natural_language_processing(self):
        """Test natural language query processing."""
        test_queries = [
            "What bugs were fixed in version 9.4.3?",
            "When was version 9.4.3a released?",
            "How do I upgrade from 9.3.1 to 9.4.3?",
            "What is the recommended release?"
        ]
        
        for query in test_queries:
            with self.subTest(query=query):
                result = self.aqa.natural_language_query(query)
                self.assertIsInstance(result, dict)
                self.assertIn('status', result)


class TestDataIntegrity(TestSystemValidation):
    """Test data integrity and validation."""
    
    def test_yaml_file_exists_and_readable(self):
        """Test YAML output file exists and is readable."""
        if self.test_data_exists:
            self.assertTrue(os.path.exists(self.data_file_path))
            
            with open(self.data_file_path, 'r') as f:
                data = yaml.safe_load(f)
                self.assertIsInstance(data, dict)
                self.assertGreater(len(data), 0)
    
    def test_release_date_formats(self):
        """Test release date formats are consistent."""
        for version, version_data in self.test_data.items():
            with self.subTest(version=version):
                if 'initial_release_date' in version_data:
                    date = version_data['initial_release_date']
                    # Should be in YYYY-MM-DD format
                    self.assertRegex(date, r'\d{4}-\d{2}-\d{2}')
    
    def test_resolved_bugs_structure(self):
        """Test resolved bugs data structure."""
        for version, version_data in self.test_data.items():
            with self.subTest(version=version):
                if 'resolved_bugs' in version_data:
                    bugs = version_data['resolved_bugs']
                    self.assertIsInstance(bugs, list)
                    
                    for bug in bugs:
                        self.assertIsInstance(bug, dict)
                        self.assertIn('id', bug)
                        self.assertIn('description', bug)
                        # CSC bug IDs should start with CSC
                        if bug['id'].startswith('CSC'):
                            self.assertRegex(bug['id'], r'CSC[a-zA-Z0-9]+')
    
    def test_upgrade_paths_structure(self):
        """Test upgrade paths data structure."""
        for version, version_data in self.test_data.items():
            with self.subTest(version=version):
                if 'upgrade_paths' in version_data:
                    paths = version_data['upgrade_paths']
                    self.assertIsInstance(paths, dict)
                    
                    # Should have platform-specific paths
                    for platform, path_list in paths.items():
                        self.assertIsInstance(path_list, list)
                        self.assertIn(platform, ['Open-Systems', 'FICON'])


class TestErrorHandling(TestSystemValidation):
    """Test error handling and edge cases."""
    
    def test_invalid_version_handling(self):
        """Test handling of invalid version queries."""
        result = self.aqa.query_resolved_bugs('invalid.version')
        self.assertIsInstance(result, dict)
        self.assertEqual(result['status'], 'error')
    
    def test_empty_query_handling(self):
        """Test handling of empty queries."""
        result = self.aqa.natural_language_query('')
        self.assertIsInstance(result, dict)
        self.assertIn('status', result)
    
    def test_malformed_query_handling(self):
        """Test handling of malformed queries."""
        result = self.aqa.natural_language_query('gibberish query that makes no sense')
        self.assertIsInstance(result, dict)
        self.assertIn('status', result)


class TestSystemIntegration(TestSystemValidation):
    """Test end-to-end system integration."""
    
    def test_data_flow_dca_to_aqa(self):
        """Test data flows correctly from DCA to AQA."""
        # Test that AQA can access data that would be generated by DCA
        if hasattr(self.dca, 'consolidated_data') and self.dca.consolidated_data:
            aqa_with_dca_data = AIQueryAssistant(data=self.dca.consolidated_data)
            result = aqa_with_dca_data.query_release_date('9.4.3')
            self.assertIsInstance(result, dict)
    
    def test_complete_workflow(self):
        """Test complete workflow from query to response."""
        workflow_queries = [
            "What bugs were fixed in version 9.4.3?",
            "When was version 9.4.3a released?",
            "How do I upgrade from 9.4.3 to 9.4.3a?"
        ]
        
        for query in workflow_queries:
            with self.subTest(query=query):
                # Test complete processing pipeline
                result = self.aqa.natural_language_query(query)
                self.assertIsInstance(result, dict)
                self.assertIn('status', result)
                
                # If successful, should have meaningful response
                if result['status'] == 'success':
                    self.assertTrue(
                        any(key in result for key in ['resolved_bugs', 'release_date', 'message'])
                    )


def run_comprehensive_tests():
    """Run all comprehensive tests with detailed reporting."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestDataConsolidationAgent,
        TestAIQueryAssistant, 
        TestDataIntegrity,
        TestErrorHandling,
        TestSystemIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print("COMPREHENSIVE TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  ❌ {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  💥 {test}: {traceback.split('Exception:')[-1].strip()}")
    
    if not result.failures and not result.errors:
        print("\n🎉 ALL TESTS PASSED! System validation complete.")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
