#!/usr/bin/env python3
"""
AI Query Assistant Test Script
Demonstrates the capabilities of the Cisco MDS Release Note AI Query Assistant
"""

import sys
import os
sys.path.append('src')

from agents.ai_query_assistant import AIQueryAssistant

def run_demo_queries():
    """Run a comprehensive demo of the AI Query Assistant capabilities."""
    
    print("🤖 Cisco MDS AI Query Assistant - Comprehensive Demo")
    print("=" * 60)
    
    # Initialize the AI Query Assistant
    aqa = AIQueryAssistant()
    
    # Demo queries to test different functionality
    test_queries = [
        "What bugs were fixed in version 9.4.3a?",
        "Show me the release date for 9.4.2a",
        "How do I upgrade from 9.3.1 to 9.4.3a?",
        "What is the recommended release for FICON?",
        "Tell me about resolved bugs in 9.2.2",
        "When was 9.4.1 released?",
        "What's the latest version available?",
        "Help me understand upgrade paths"
    ]
    
    print(f"Running {len(test_queries)} test queries...\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"📋 Test {i}/{len(test_queries)}: {query}")
        print("-" * 50)
        
        try:
            response = aqa.natural_language_query(query)
            aqa._display_response(response)
        except Exception as e:
            print(f"❌ Error processing query: {str(e)}")
        
        print()
    
    # Test specific method calls
    print("🔧 Testing Direct Method Calls")
    print("=" * 40)
    
    try:
        print("1. Testing query_resolved_bugs('9.4.3'):")
        result = aqa.query_resolved_bugs('9.4.3')
        print(f"   Status: {result.get('status')}")
        print(f"   Bugs found: {result.get('total_bugs_resolved', 0)}")
        
        print("\n2. Testing query_release_date('9.4.3a'):")
        result = aqa.query_release_date('9.4.3a')
        print(f"   Status: {result.get('status')}")
        print(f"   Release Date: {result.get('release_date')}")
        
        print("\n3. Testing query_upgrade_path('9.3.1', '9.4.3'):")
        result = aqa.query_upgrade_path('9.3.1', '9.4.3')
        print(f"   Status: {result.get('status')}")
        print(f"   Message: {result.get('message', 'Direct upgrade available' if result.get('status') == 'success' else 'See details')}")
        
    except Exception as e:
        print(f"❌ Error in direct method testing: {str(e)}")
    
    print("\n✅ Demo completed successfully!")
    print("\nNext steps:")
    print("- Use aqa.start_interactive_session() for live queries")
    print("- Import AIQueryAssistant for programmatic access")
    print("- Extend with additional query types as needed")

if __name__ == "__main__":
    run_demo_queries()
