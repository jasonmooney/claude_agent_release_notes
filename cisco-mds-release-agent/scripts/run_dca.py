# File: /cisco-mds-release-agent/cisco-mds-release-agent/scripts/run_dca.py

import sys
from src.agents.data_consolidation_agent import DataConsolidationAgent
from src.utils.logger import setup_logging

def main():
    # Set up logging
    setup_logging()

    # Initialize the Data Consolidation Agent
    dca = DataConsolidationAgent()

    # Run the Data Consolidation Agent
    try:
        dca.run()
    except Exception as e:
        print(f"An error occurred while running the Data Consolidation Agent: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()