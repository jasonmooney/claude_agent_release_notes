import sys
from agents.data_consolidation_agent import DataConsolidationAgent
from agents.ai_query_assistant import AIQueryAssistant

def main():
    print("Starting Cisco MDS Release Note Agentic System...")
    
    # Initialize the Data Consolidation Agent
    print("Initializing Data Consolidation Agent...")
    dca = DataConsolidationAgent()
    dca.run()
    print("Data Consolidation Agent completed.")

    # Initialize the AI Query Assistant
    print("Initializing AI Query Assistant...")
    aqa = AIQueryAssistant(dca.consolidated_data)
    print("AI Query Assistant initialized.")
    
    print("\nSystem initialized successfully!")
    print("Available query methods:")
    print("- query_upgrade_path(current_version, target_version)")
    print("- query_recommended_release(platform)")
    print("- query_resolved_bugs(version)")
    print("- query_release_date(version)")
    print("- natural_language_query(query_string)")
    
    # Demonstrate AI Query functionality
    print("\n" + "="*60)
    print("🤖 AI QUERY ASSISTANT DEMONSTRATION")
    print("="*60)
    
    # Example queries
    demo_queries = [
        "What bugs were fixed in version 9.4.3?",
        "How do I upgrade from 9.2.2 to 9.4.3?", 
        "When was version 9.4.3a released?",
        "What is the recommended release for open systems?"
    ]
    
    for query in demo_queries:
        print(f"\n❓ Demo Query: {query}")
        print("🔍 Processing...")
        response = aqa.natural_language_query(query)
        aqa._display_response(response)
    
    print("\n" + "="*60)
    print("🎯 Ready for Interactive Queries!")
    print("="*60)
    print("You can now:")
    print("1. Use the interactive session: aqa.start_interactive_session()")
    print("2. Make direct queries: aqa.natural_language_query('your question')")
    print("3. Use specific methods like: aqa.query_resolved_bugs('9.4.3')")
    
    # Ask user if they want to start interactive session
    try:
        user_choice = input("\nWould you like to start an interactive query session? (y/n): ").strip().lower()
        if user_choice in ['y', 'yes']:
            aqa.start_interactive_session()
        else:
            print("System ready. You can import and use the AIQueryAssistant class for programmatic queries.")
    except KeyboardInterrupt:
        print("\nSystem ready for programmatic use.")

if __name__ == "__main__":
    main()