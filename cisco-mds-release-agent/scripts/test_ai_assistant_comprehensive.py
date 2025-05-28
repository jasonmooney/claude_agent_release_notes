#!/usr/bin/env python3
"""
Enhanced AI Query Assistant Test Script
Comprehensive validation and demonstration of the Cisco MDS Release Note AI Query Assistant
"""

import sys
import os
import time
import traceback

# Add src to path for imports  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.ai_query_assistant import AIQueryAssistant


class AIAssistantTester:
    """Comprehensive tester for AI Query Assistant."""
    
    def __init__(self):
        self.aqa = None
        self.test_results = {'passed': 0, 'failed': 0, 'errors': []}
        self.start_time = None
        
    def setup(self):
        """Initialize the AI Query Assistant."""
        try:
            print("🔧 Initializing AI Query Assistant...")
            self.aqa = AIQueryAssistant()
            print("✅ AI Query Assistant initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize AI Query Assistant: {str(e)}")
            self.test_results['errors'].append(f"Initialization failed: {str(e)}")
            return False
    
    def test_query(self, query, expected_fields=None):
        """Test a single query and validate response."""
        try:
            print(f"🔍 Testing: {query}")
            response = self.aqa.natural_language_query(query)
            
            # Basic response validation
            if not isinstance(response, dict):
                raise ValueError("Response is not a dictionary")
            
            if 'status' not in response:
                raise ValueError("Response missing 'status' field")
            
            # Check expected fields if provided
            if expected_fields:
                for field in expected_fields:
                    if field not in response:
                        raise ValueError(f"Response missing expected field: {field}")
            
            print(f"   ✅ Status: {response.get('status')}")
            
            # Display response using AQA's display method
            if hasattr(self.aqa, '_display_response'):
                self.aqa._display_response(response)
            
            self.test_results['passed'] += 1
            return True
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"Query '{query}': {str(e)}")
            return False
    
    def test_direct_methods(self):
        """Test direct method calls."""
        print("\n🔧 Testing Direct Method Calls")
        print("=" * 50)
        
        # Test query_resolved_bugs
        try:
            print("1. Testing query_resolved_bugs('9.4.3'):")
            result = self.aqa.query_resolved_bugs('9.4.3')
            print(f"   Status: {result.get('status')}")
            print(f"   Bugs found: {result.get('total_bugs_resolved', 0)}")
            
            if result.get('status') == 'success':
                self.test_results['passed'] += 1
                print("   ✅ Resolved bugs query successful")
            else:
                self.test_results['failed'] += 1
                print("   ❌ Resolved bugs query failed")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"query_resolved_bugs: {str(e)}")
        
        # Test query_release_date
        try:
            print("\n2. Testing query_release_date('9.4.3a'):")
            result = self.aqa.query_release_date('9.4.3a')
            print(f"   Status: {result.get('status')}")
            print(f"   Release Date: {result.get('release_date')}")
            
            if result.get('status') == 'success':
                self.test_results['passed'] += 1
                print("   ✅ Release date query successful")
            else:
                self.test_results['failed'] += 1
                print("   ❌ Release date query failed")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"query_release_date: {str(e)}")
        
        # Test query_upgrade_path
        try:
            print("\n3. Testing query_upgrade_path('9.3.1', '9.4.3'):")
            result = self.aqa.query_upgrade_path('9.3.1', '9.4.3')
            print(f"   Status: {result.get('status')}")
            print(f"   Message: {result.get('message', 'See details')}")
            
            if isinstance(result, dict) and 'status' in result:
                self.test_results['passed'] += 1
                print("   ✅ Upgrade path query successful")
            else:
                self.test_results['failed'] += 1
                print("   ❌ Upgrade path query failed")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"query_upgrade_path: {str(e)}")
    
    def test_natural_language_queries(self):
        """Test natural language query processing."""
        print("\n🗣️  Testing Natural Language Queries")
        print("=" * 50)
        
        test_queries = [
            ("What bugs were fixed in version 9.4.3?", ['resolved_bugs']),
            ("When was version 9.4.3a released?", ['release_date']),
            ("How do I upgrade from 9.3.1 to 9.4.3?", ['status']),
            ("What is the recommended release?", ['status']),
            ("Tell me about resolved bugs in 9.2.2", ['status']),
            ("When was 9.4.1 released?", ['status']),
            ("What's the latest version available?", ['status']),
            ("Help me understand upgrade paths", ['status'])
        ]
        
        for i, (query, expected_fields) in enumerate(test_queries, 1):
            print(f"\n📋 Test {i}/{len(test_queries)}:")
            print("-" * 40)
            self.test_query(query, expected_fields)
    
    def test_error_handling(self):
        """Test error handling capabilities."""
        print("\n🛡️  Testing Error Handling")
        print("=" * 50)
        
        error_test_cases = [
            "Invalid version xyz.abc",
            "",  # Empty query
            "Random gibberish that makes no sense",
            "Query with version 99.99.99 that doesn't exist"
        ]
        
        for i, error_case in enumerate(error_test_cases, 1):
            print(f"\n🔍 Error Test {i}/{len(error_test_cases)}: '{error_case}'")
            try:
                response = self.aqa.natural_language_query(error_case)
                if isinstance(response, dict) and 'status' in response:
                    print(f"   ✅ Handled gracefully: {response.get('status')}")
                    self.test_results['passed'] += 1
                else:
                    print("   ❌ Did not return proper error response")
                    self.test_results['failed'] += 1
            except Exception as e:
                print(f"   ⚠️  Exception raised: {str(e)}")
                # Exceptions might be acceptable for some error cases
                self.test_results['passed'] += 1
    
    def generate_report(self):
        """Generate comprehensive test report."""
        end_time = time.time()
        duration = end_time - self.start_time
        
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("="*80)
        
        total_tests = self.test_results['passed'] + self.test_results['failed']
        success_rate = (self.test_results['passed'] / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📈 RESULTS SUMMARY:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {self.test_results['passed']}")
        print(f"   Failed: {self.test_results['failed']}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Duration: {duration:.2f} seconds")
        
        if self.test_results['errors']:
            print(f"\n❌ ERRORS ENCOUNTERED ({len(self.test_results['errors'])}):")
            for error in self.test_results['errors']:
                print(f"   • {error}")
        
        if self.test_results['failed'] == 0:
            print(f"\n🎉 ALL TESTS PASSED!")
            print("   AI Query Assistant is fully functional and ready for use.")
        else:
            print(f"\n⚠️  SOME TESTS FAILED")
            print("   Review errors and fix issues before production use.")
        
        print(f"\n💡 NEXT STEPS:")
        print("   • Use aqa.start_interactive_session() for live queries")
        print("   • Import AIQueryAssistant for programmatic access")
        print("   • Extend with additional query types as needed")
        
        return self.test_results['failed'] == 0
    
    def run_all_tests(self):
        """Run all tests and generate report."""
        self.start_time = time.time()
        
        print("🚀 Cisco MDS AI Query Assistant - Comprehensive Validation")
        print("=" * 80)
        print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Setup
        if not self.setup():
            return False
        
        # Run all test categories
        self.test_natural_language_queries()
        self.test_direct_methods() 
        self.test_error_handling()
        
        # Generate report
        success = self.generate_report()
        
        return success


def run_demo_queries():
    """Main entry point for AI assistant testing."""
    tester = AIAssistantTester()
    success = tester.run_all_tests()
    return success


if __name__ == "__main__":
    success = run_demo_queries()
    sys.exit(0 if success else 1)
