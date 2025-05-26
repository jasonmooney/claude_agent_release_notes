# File: /cisco-mds-release-agent/cisco-mds-release-agent/src/main.py

import sys
from agents.data_consolidation_agent import DataConsolidationAgent
from agents.ai_query_assistant import AIQueryAssistant

def main():
    # Initialize the Data Consolidation Agent
    dca = DataConsolidationAgent()
    dca.run()

    # Initialize the AI Query Assistant
    aqa = AIQueryAssistant(dca.get_consolidated_data())
    aqa.start_interaction()

if __name__ == "__main__":
    main()