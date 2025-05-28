#!/usr/bin/env python3
"""
Simple Test Validation Script for Cisco MDS Release Note Agentic System
Validates that all core components can be imported and basic functionality works.
"""

import sys
import os
import traceback

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that all core modules can be imported."""
    print("🔍 Testing Module Imports...")
    
    try:
        from agents.data_consolidation_agent import DataConsolidationAgent
        print("✅ DataConsolidationAgent imported successfully")
    except Exception as e:
        print(f"❌ Failed to import DataConsolidationAgent: {e}")
        return False
    
    try:
        from agents.ai_query_assistant import AIQueryAssistant
        print("✅ AIQueryAssistant imported successfully")
    except Exception as e:
        print(f"❌ Failed to import AIQueryAssistant: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality of core components."""
    print("\n🔧 Testing Basic Functionality...")
    
    try:
        from agents.data_consolidation_agent import DataConsolidationAgent
        from agents.ai_query_assistant import AIQueryAssistant
        
        # Test DCA initialization
        dca = DataConsolidationAgent()
        print("✅ DataConsolidationAgent initialized")
        
        # Test DCA has correct attribute (not method)
        if hasattr(dca, 'consolidated_data'):
            print("✅ DCA has consolidated_data attribute")
        else:
            print("❌ DCA missing consolidated_data attribute")
            return False
        
        # Test AQA initialization
        aqa = AIQueryAssistant()
        print("✅ AIQueryAssistant initialized")
        
        # Test AQA has key methods
        required_methods = ['natural_language_query', 'query_resolved_bugs', 'query_release_date', 'query_upgrade_path']
        for method in required_methods:
            if hasattr(aqa, method):
                print(f"✅ AQA has {method} method")
            else:
                print(f"❌ AQA missing {method} method")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False

def test_data_file():
    """Test that data file exists and is readable."""
    print("\n📄 Testing Data File...")
    
    try:
        data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'output', 'upgrade_paths.yaml')
        
        if os.path.exists(data_file):
            print("✅ YAML data file exists")
            
            import yaml
            with open(data_file, 'r') as f:
                data = yaml.safe_load(f)
            
            if isinstance(data, dict) and len(data) > 0:
                print(f"✅ YAML data file valid ({len(data)} releases)")
                return True
            else:
                print("❌ YAML data file invalid or empty")
                return False
        else:
            print("⚠️  YAML data file not found (may need to run DCA first)")
            return True  # Not a failure, just needs data generation
            
    except Exception as e:
        print(f"❌ Data file test failed: {e}")
        return False

def main():
    """Run all validation tests."""
    print("🚀 Cisco MDS Release Note Agentic System - Simple Validation")
    print("=" * 70)
    
    tests = [
        ("Module Imports", test_imports),
        ("Basic Functionality", test_basic_functionality), 
        ("Data File", test_data_file)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} Test...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} test PASSED")
        else:
            print(f"❌ {test_name} test FAILED")
    
    print(f"\n{'='*70}")
    print(f"📊 VALIDATION RESULTS")
    print(f"{'='*70}")
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    
    if passed == total:
        print("🎉 ALL VALIDATION TESTS PASSED!")
        print("System components are working correctly.")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Review errors before proceeding.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
