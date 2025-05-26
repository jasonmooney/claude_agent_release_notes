# User Guide for Cisco MDS Release Note Agentic System

## Introduction
Welcome to the user guide for the Cisco MDS Release Note Agentic System. This document provides an overview of the system's functionality, how to set it up, and how to use it effectively.

## Overview
The Cisco MDS Release Note Agentic System is designed to automate the consolidation and interpretation of Cisco MDS 9000 series device release information. It consists of two main components:

1. **Data Consolidation Agent (DCA)**: This agent fetches, parses, and structures information from various Cisco MDS release note documents.
2. **AI Query Assistant (AQA)**: This component provides a natural language interface for users to query the consolidated data.

## System Requirements
- Python 3.x
- Required Python packages (see `requirements.txt` for details)
- Access to the internet for fetching release notes

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd cisco-mds-release-agent
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy `.env.example` to `.env` and fill in the necessary values.

## Usage
### Running the Data Consolidation Agent
To run the Data Consolidation Agent, execute the following command:
```
python scripts/run_dca.py
```
This will initiate the process of fetching and consolidating release notes.

### Querying Data with the AI Query Assistant
Once the data has been consolidated, you can interact with the AI Query Assistant. You can ask questions such as:
- "What is the upgrade path from version X.Y(Za) to Z.A(Bc) for Open-Systems?"
- "What bugs were fixed in version 9.4(3a)?"

### Accessing Logs and Cached Data
- Logs are stored in the `data/logs` directory.
- Cached release note files can be found in the `data/cache` directory.

## Troubleshooting
- Ensure that all dependencies are installed correctly.
- Check the logs for any errors during the fetching or parsing process.
- If you encounter issues, refer to the `CHANGE.md` file for recent updates or changes.

## Conclusion
This user guide provides a comprehensive overview of the Cisco MDS Release Note Agentic System. For further assistance, please refer to the API documentation or contact the project maintainers.