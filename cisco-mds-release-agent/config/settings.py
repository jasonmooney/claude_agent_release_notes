# settings.py

# Configuration settings for the Cisco MDS Release Note Agentic System

import os

class Config:
    # General settings
    PROJECT_NAME = "Cisco MDS Release Note Agentic System"
    VERSION = "1.0"
    
    # File paths
    CACHE_DIR = os.path.join(os.path.dirname(__file__), '../data/cache')
    LOG_DIR = os.path.join(os.path.dirname(__file__), '../data/logs')
    OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '../data/output/upgrade_paths.yaml')
    
    # Web scraping settings
    BASE_URL = "https://www.cisco.com"
    RELEASE_NOTES_INDEX_URL = f"{BASE_URL}/c/en/us/support/storage-networking/mds-9000-nx-os-san-os-software/products-release-notes-list.html"
    RECOMMENDED_RELEASES_URL = f"{BASE_URL}/c/en/us/td/docs/switches/datacenter/mds9000/sw/b_MDS_NX-OS_Recommended_Releases.html"
    
    # Logging settings
    LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    # Caching settings
    CACHE_EXPIRY_DAYS = 7  # Number of days to keep cached files

    # Environment variables
    ENV_FILE = os.path.join(os.path.dirname(__file__), '.env')  # Path to the .env file for sensitive information

# Load environment variables from .env file if it exists
if os.path.exists(Config.ENV_FILE):
    from dotenv import load_dotenv
    load_dotenv(Config.ENV_FILE)