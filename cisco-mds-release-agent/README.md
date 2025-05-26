# README.md

# Cisco MDS Release Note Agentic System

## Overview
The Cisco MDS Release Note Agentic System is designed to automate the consolidation and interpretation of release information for Cisco MDS 9000 series devices. This system aims to empower Cisco TAC engineers and customers by providing quick and accurate access to upgrade/downgrade paths, recommended NX-OS releases, defect fixes, and relevant release dates.

## Project Structure
The project is organized into several directories and files, each serving a specific purpose:

- **src/**: Contains the main application code.
  - **agents/**: Implements the core functionalities of the Data Consolidation Agent and AI Query Assistant.
  - **parsers/**: Handles the parsing of various release notes.
  - **data/**: Defines data models and handles YAML file operations.
  - **utils/**: Provides utility functions for web scraping, caching, and logging.
  - **main.py**: The entry point for the application.

- **tests/**: Contains unit tests for the application components to ensure functionality and reliability.

- **data/**: Stores cached files, logs, and the output YAML file containing structured data.

- **config/**: Holds configuration settings and environment variable examples.

- **docs/**: Provides documentation, including the System Requirements Specification (SRS), API documentation, and user guide.

- **scripts/**: Contains scripts for setting up the environment and running the Data Consolidation Agent.

- **requirements.txt**: Lists the dependencies required for the project.

- **setup.py**: Used for packaging the application and managing dependencies.

- **.gitignore**: Specifies files and directories to be ignored by Git.

- **CHANGE.md**: Tracks changes made to the project.

## Getting Started
To get started with the Cisco MDS Release Note Agentic System, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd cisco-mds-release-agent
   ```

2. Set up the environment:
   ```
   bash scripts/setup.sh
   ```

3. Run the application:
   ```
   python src/main.py
   ```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.