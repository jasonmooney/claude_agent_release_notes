#!/usr/bin/env python3
"""
Master Test Runner for Cisco MDS Release Note Agentic System
Runs all tests and provides comprehensive validation reporting.
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))


class TestRunner:
    """Orchestrates all system tests and validation."""
    
    def __init__(self):
        self.project_root = project_root
        self.test_results = {}
        self.start_time = None
        self.end_time = None
    
    def print_header(self, title):
        """Print formatted test section header."""
        print(f"\n{'='*80}")
        print(f"🧪 {title}")
        print(f"{'='*80}")
    
    def print_subheader(self, title):
        """Print formatted test subsection header."""
        print(f"\n{'-'*60}")
        print(f"📋 {title}")
        print(f"{'-'*60}")
    
    def run_unit_tests(self):
        """Run all unit tests."""
        self.print_subheader("Running Unit Tests")
        
        # Run comprehensive validation tests
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pytest', 
                'tests/test_comprehensive_validation.py', 
                '-v', '--tb=short'
            ], cwd=self.project_root, capture_output=True, text=True, timeout=300)
            
            self.test_results['unit_tests'] = {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
            
            if result.returncode == 0:
                print("✅ Unit tests passed")
            else:
                print("❌ Unit tests failed")
                print(f"Error output: {result.stderr}")
            
        except subprocess.TimeoutExpired:
            print("⏰ Unit tests timed out")
            self.test_results['unit_tests'] = {'success': False, 'error': 'timeout'}
        except Exception as e:
            print(f"💥 Error running unit tests: {str(e)}")
            self.test_results['unit_tests'] = {'success': False, 'error': str(e)}
    
    def run_integration_tests(self):
        """Run integration tests."""
        self.print_subheader("Running Integration Tests")
        
        try:
            # Test the AI assistant demo script
            result = subprocess.run([
                sys.executable, 'scripts/test_ai_assistant.py'
            ], cwd=self.project_root, capture_output=True, text=True, timeout=120)
            
            self.test_results['integration_tests'] = {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
            
            if result.returncode == 0:
                print("✅ Integration tests passed")
            else:
                print("❌ Integration tests failed")
                print(f"Error output: {result.stderr}")
            
        except subprocess.TimeoutExpired:
            print("⏰ Integration tests timed out")
            self.test_results['integration_tests'] = {'success': False, 'error': 'timeout'}
        except Exception as e:
            print(f"💥 Error running integration tests: {str(e)}")
            self.test_results['integration_tests'] = {'success': False, 'error': str(e)}
    
    def run_system_validation(self):
        """Run full system validation."""
        self.print_subheader("Running System Validation")
        
        try:
            # Test main.py execution
            result = subprocess.run([
                sys.executable, 'src/main.py'
            ], cwd=self.project_root, input='n\n', capture_output=True, text=True, timeout=300)
            
            self.test_results['system_validation'] = {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
            
            if result.returncode == 0:
                print("✅ System validation passed")
                # Check for key success indicators in output
                output = result.stdout
                success_indicators = [
                    "Data consolidation completed successfully!",
                    "AI Query Assistant initialized",
                    "System initialized successfully!"
                ]
                
                for indicator in success_indicators:
                    if indicator in output:
                        print(f"   ✓ {indicator}")
                    else:
                        print(f"   ⚠️  Missing indicator: {indicator}")
            else:
                print("❌ System validation failed")
                print(f"Error output: {result.stderr}")
            
        except subprocess.TimeoutExpired:
            print("⏰ System validation timed out")
            self.test_results['system_validation'] = {'success': False, 'error': 'timeout'}
        except Exception as e:
            print(f"💥 Error running system validation: {str(e)}")
            self.test_results['system_validation'] = {'success': False, 'error': str(e)}
    
    def validate_data_integrity(self):
        """Validate data integrity and structure."""
        self.print_subheader("Validating Data Integrity")
        
        try:
            # Check if YAML output file exists and is valid
            yaml_file = self.project_root / 'data' / 'output' / 'upgrade_paths.yaml'
            
            if yaml_file.exists():
                import yaml
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                
                if isinstance(data, dict) and len(data) > 0:
                    print(f"✅ YAML data file valid ({len(data)} releases)")
                    
                    # Validate data structure
                    sample_version = list(data.keys())[0]
                    sample_data = data[sample_version]
                    
                    required_fields = ['initial_release_date', 'resolved_bugs', 'upgrade_paths']
                    for field in required_fields:
                        if field in sample_data:
                            print(f"   ✓ Contains {field}")
                        else:
                            print(f"   ⚠️  Missing {field}")
                    
                    self.test_results['data_integrity'] = {'success': True, 'releases': len(data)}
                else:
                    print("❌ YAML data file invalid or empty")
                    self.test_results['data_integrity'] = {'success': False, 'error': 'invalid_data'}
            else:
                print("❌ YAML data file not found")
                self.test_results['data_integrity'] = {'success': False, 'error': 'file_not_found'}
        
        except Exception as e:
            print(f"💥 Error validating data integrity: {str(e)}")
            self.test_results['data_integrity'] = {'success': False, 'error': str(e)}
    
    def check_dependencies(self):
        """Check that all dependencies are installed."""
        self.print_subheader("Checking Dependencies")
        
        required_packages = [
            'requests', 'beautifulsoup4', 'pyyaml', 're', 'datetime', 'logging'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"   ✓ {package}")
            except ImportError:
                print(f"   ❌ {package} (missing)")
                missing_packages.append(package)
        
        self.test_results['dependencies'] = {
            'success': len(missing_packages) == 0,
            'missing': missing_packages
        }
        
        if not missing_packages:
            print("✅ All dependencies satisfied")
        else:
            print(f"❌ Missing dependencies: {', '.join(missing_packages)}")
    
    def generate_report(self):
        """Generate comprehensive test report."""
        self.print_header("COMPREHENSIVE TEST REPORT")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result.get('success', False))
        
        print(f"\n📊 OVERALL RESULTS:")
        print(f"   Total Test Categories: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {total_tests - passed_tests}")
        print(f"   Success Rate: {(passed_tests / total_tests * 100):.1f}%")
        print(f"   Duration: {(self.end_time - self.start_time):.1f} seconds")
        
        print(f"\n📋 DETAILED RESULTS:")
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result.get('success', False) else "❌ FAIL"
            print(f"   {status} {test_name.replace('_', ' ').title()}")
            
            if not result.get('success', False) and 'error' in result:
                print(f"     Error: {result['error']}")
        
        # System status
        if passed_tests == total_tests:
            print(f"\n🎉 SYSTEM STATUS: FULLY OPERATIONAL")
            print("   All tests passed. System ready for production use.")
        else:
            print(f"\n⚠️  SYSTEM STATUS: ISSUES DETECTED")
            print("   Some tests failed. Review errors before production use.")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """Run all tests and generate report."""
        self.start_time = time.time()
        
        self.print_header("CISCO MDS RELEASE NOTE AGENTIC SYSTEM - COMPREHENSIVE TEST SUITE")
        print(f"🚀 Starting comprehensive validation at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all test categories
        self.check_dependencies()
        self.validate_data_integrity()
        self.run_unit_tests()
        self.run_integration_tests()
        self.run_system_validation()
        
        self.end_time = time.time()
        
        # Generate final report
        success = self.generate_report()
        
        return success


def main():
    """Main entry point for test runner."""
    runner = TestRunner()
    success = runner.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
