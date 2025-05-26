# System Requirements Specification (SRS) for Cisco MDS Release Note Agentic System

## Version
1.0

## Date
May 25, 2025

## Project Owner
(Your Name/Team)

## 1. Introduction

### 1.1 Project Vision
To develop an advanced agentic system that automates the consolidation and interpretation of Cisco MDS 9000 series device release information. This system will empower Cisco TAC engineers and customers to quickly and accurately determine upgrade/downgrade paths, identify currently recommended NX-OS releases, understand defect fixes between versions, and access relevant release and recommendation dates.

### 1.2 Project Goals
- Develop a robust Data Consolidation Agent (DCA) to autonomously gather, parse, and structure information from various Cisco MDS release note documents.
- Develop an intelligent AI Query Assistant (AQA) that leverages the consolidated data to answer user queries in natural language.
- Ensure data accuracy and timeliness through regular updates and comprehensive parsing logic.
- Provide a reliable and efficient tool that reduces manual research time and improves decision-making for MDS software management.
- Design a maintainable and scalable system.

### 1.3 Scope

#### In Scope
- Processing of Cisco MDS 9000 Series Release Notes (NX-OS/SAN-OS), EPLD Release Notes, Transceiver Firmware Release Notes, and the official "Recommended Releases for Cisco MDS 9000 Series Switches" page.
- Extraction of Open-Systems and FICON upgrade/downgrade paths.
- Extraction of recommended release information (Open-Systems and FICON), prioritizing "With Smart Licensing" versions.
- Extraction of resolved defect (Bug ID) information from NX-OS release notes.
- Extraction of initial release dates for software versions and EPLDs.
- Extraction of dates when specific versions became "recommended."
- Storing consolidated data in a structured YAML format.
- Answering user queries via an LLM-powered interface regarding the extracted information.
- Caching mechanism for fetched data.
- Integration with Langchain, Langsmith, and a specified Google Gemini LLM.
- Adherence to specified development environment and coding standards (Python 3, venv, WSL Ubuntu, PEP 8).
- Version control using Git with the specified repository.
- Okta integration for potential future secured access (details to be confirmed for specific agent interfaces if needed).

#### Out of Scope
- Processing release notes for products other than Cisco MDS 9000 series.
- Real-time alerts for new release note publications (system will rely on scheduled refreshes).
- Direct integration with Cisco TAC case management systems (AQA is a standalone query tool).
- Automated software deployment or switch configuration.
- Parsing of "Storage Services Interface Image Release" notes (these should be explicitly skipped).

### 1.4 Definitions, Acronyms, and Abbreviations
- **DCA**: Data Consolidation Agent
- **AQA**: AI Query Assistant
- **LLM**: Large Language Model
- **SRS**: Software Requirements Specification
- **MDS**: Multilayer Director Switch (Cisco 9000 Series)
- **NX-OS**: Cisco's Network Operating System for MDS
- **SAN-OS**: Older name for NX-OS
- **EPLD**: Electronic Programmable Logic Device
- **FICON**: Fibre Connection (IBM mainframe protocol)
- **Open-Systems**: Non-FICON environments
- **TAC**: Technical Assistance Center (Cisco)
- **YAML**: YAML Ain't Markup Language (data serialization format)
- **API**: Application Programming Interface
- **URL**: Uniform Resource Locator
- **PEP 8**: Style Guide for Python Code

## 2. System Architecture Overview
The system will consist of two distinct, decoupled agents:

### 2.1 Data Consolidation Agent (DCA)
- **Purpose**: This agent is responsible for all interactions with the Cisco website, fetching raw release note documents (HTML and PDF as appropriate), parsing them, extracting relevant information, structuring this information, and saving it into a central, well-defined data store (YAML file).
- **Characteristics**: Primarily a backend, automated process. Focus on robust parsing, data accuracy, and efficient data transformation.

### 2.2 AI Query Assistant (AQA)
- **Purpose**: This agent provides a natural language interface for users to ask questions about the data consolidated by the DCA. It uses an LLM, contextualized with the data from the YAML file, to generate answers.
- **Characteristics**: User-facing (potentially via CLI or a simple API initially). Focus on natural language understanding, accurate information retrieval from the structured data, and clear, helpful response generation.

### 2.3 Rationale for Decoupling
- **Maintainability**: Allows independent development, testing, and updating of data extraction logic (DCA) and AI interaction logic (AQA).
- **Scalability**: Data processing and query handling can be scaled independently.
- **Flexibility**: The structured data output from DCA could potentially be used by other tools or systems in the future, not just the AQA. The AQA could also potentially leverage different LLMs or data sources with modifications.
- **Robustness**: Issues in one agent are less likely to directly impact the other (e.g., if a Cisco webpage changes format, only DCA needs updating; AQA continues to work with the last good dataset).

## 3. Detailed Requirements: Data Consolidation Agent (DCA)
### 3.1 Objective
To autonomously and accurately extract all specified information from Cisco MDS 9000 series release documentation and store it in a structured, version-controlled YAML file.

### 3.2 Primary Data Sources
- **Main Release Notes Index URL**: https://www.cisco.com/c/en/us/support/storage-networking/mds-9000-nx-os-san-os-software/products-release-notes-list.html
- **Recommended Releases Page URL**: https://www.cisco.com/c/en/us/td/docs/switches/datacenter/mds9000/sw/b_MDS_NX-OS_Recommended_Releases.html

### 3.3 Core Functionality & Logic
#### 3.3.1 Release Note Discovery
- The DCA shall periodically scan the Main Release Notes Index URL to identify links to individual release note documents.
- It shall classify links into:
  - Cisco MDS 9000 Series Release Notes (NX-OS/SAN-OS)
  - Cisco MDS 9000 Series EPLD Release Notes
  - Cisco MDS 9000 Series Transceiver Firmware Release Notes
- It shall explicitly skip any links identified as "Cisco MDS 9000 Family Release Notes for Storage Services Interface Image Release."

#### 3.3.2 Document Fetching & Pre-processing
- The DCA shall download the content of identified release notes. HTML format is preferred if available; PDF parsing capabilities may be required as a fallback for older documents or specific information types not well-represented in HTML.
- Downloaded files shall be stored locally temporarily for processing.
- **Filename Normalization**: All saved release note files must follow a consistent naming convention that includes the version and type.

#### 3.3.3 Data Extraction
- For each NX-OS release note, extract the specific NX-OS version, initial release date, upgrade paths, and resolved issues.
- For EPLD and Transceiver Firmware release notes, extract relevant identifiers, release dates, and supported versions.

### 3.4 Data Structuring & Output (YAML Format)
- All extracted data shall be consolidated into a single YAML file named `upgrade_paths.yaml`.

### 3.5 Caching & Refresh Mechanism
- The DCA shall cache downloaded release note files to avoid re-fetching unchanged documents.

### 3.6 Error Handling & Logging
- Log all major operations, errors, and warnings to a local log file.

### 3.7 Development & Operational Environment
- Python 3 (latest stable).
- Operate within a Python virtual environment (venv).
- All Python code must adhere to PEP 8 standards.

## 4. Detailed Requirements: AI Query Assistant (AQA)
### 4.1 Objective
To provide an intelligent, natural language interface for users to query the consolidated Cisco MDS release information.

### 4.2 Input Data Source
The AQA shall exclusively use the `upgrade_paths.yaml` file generated by the DCA as its knowledge base.

### 4.3 Core Capabilities (Query Types)
- Upgrade/Downgrade Paths
- Recommended Releases
- Defect (Bug Fix) Information
- Release Dates & Timelines

### 4.4 LLM Integration
- Framework: Langchain shall be used to manage interactions with the LLM.

### 4.5 System Prompt Engineering
The quality of AQA responses heavily depends on the system prompt, which must instruct the LLM on its persona and knowledge source.