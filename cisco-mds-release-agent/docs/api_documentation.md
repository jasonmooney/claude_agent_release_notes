# API Documentation for Cisco MDS Release Note Agentic System

## Overview

The Cisco MDS Release Note Agentic System provides a structured approach to automate the consolidation and interpretation of Cisco MDS 9000 series device release information. This document outlines the API endpoints available for interacting with the system.

## Base URL

```
http://<hostname>:<port>/api
```

## Endpoints

### 1. Get Release Notes

- **Endpoint:** `/release-notes`
- **Method:** `GET`
- **Description:** Retrieves a list of all available release notes.
- **Response:**
  - **200 OK**
    - Content: 
      ```json
      {
        "release_notes": [
          {
            "version": "9.4(3a)",
            "type": "NX-OS",
            "release_date": "2025-05-25"
          },
          ...
        ]
      }
      ```

### 2. Get Upgrade Path

- **Endpoint:** `/upgrade-path`
- **Method:** `POST`
- **Description:** Retrieves the upgrade path from a specified source version to a target version.
- **Request Body:**
  ```json
  {
    "source_version": "8.4(2f)",
    "target_version": "9.4(3a)"
  }
  ```
- **Response:**
  - **200 OK**
    - Content:
      ```json
      {
        "upgrade_path": [
          {
            "step": "Upgrade to 8.4(2c)",
            "description": "Required intermediate upgrade."
          },
          {
            "step": "Upgrade to 9.4(3a)",
            "description": "Final upgrade step."
          }
        ]
      }
      ```
  - **400 Bad Request**
    - Content:
      ```json
      {
        "error": "Invalid version format."
      }
      ```

### 3. Get Recommended Releases

- **Endpoint:** `/recommended-releases`
- **Method:** `GET`
- **Description:** Retrieves the current recommended releases for Open-Systems and FICON environments.
- **Response:**
  - **200 OK**
    - Content:
      ```json
      {
        "recommended_releases": {
          "open_systems": {
            "version": "9.4(3a)",
            "recommended_since": "2025-05-25"
          },
          "ficon": {
            "version": "9.4(1a)",
            "recommended_since": "2025-05-20"
          }
        }
      }
      ```

### 4. Get Bug Fix Information

- **Endpoint:** `/bug-fixes`
- **Method:** `POST`
- **Description:** Retrieves information about bugs fixed between two specified versions.
- **Request Body:**
  ```json
  {
    "from_version": "8.4(2a)",
    "to_version": "8.4(2f)"
  }
  ```
- **Response:**
  - **200 OK**
    - Content:
      ```json
      {
        "fixed_bugs": [
          {
            "id": "CSCxx12345",
            "description": "Memory leak fixed in XYZ process."
          },
          ...
        ]
      }
      ```

## Error Handling

All error responses will include an appropriate HTTP status code and a JSON object containing an error message.

## Conclusion

This API documentation provides a comprehensive overview of the endpoints available for interacting with the Cisco MDS Release Note Agentic System. For further details, please refer to the source code or contact the development team.