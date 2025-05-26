# File: /cisco-mds-release-agent/cisco-mds-release-agent/src/main.py

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
    
    # For now, just demonstrate that the system is working
    print("\nSystem is ready for queries. Implementation complete.")

if __name__ == "__main__":
    main()