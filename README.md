# Octane-to-Oracle Feature Integration

## Overview

Octane-to-Oracle Feature Integration is a Python-based data integration tool designed to extract Feature information from OpenText ALM Octane through REST APIs, transform the retrieved data, and synchronize it into an Oracle database.

The solution provides a centralized and structured data source for reporting, analytics, and downstream system integration.

### Key Features

- **Automated Data Extraction** – Retrieves Feature records from OpenText ALM Octane through REST APIs.
- **Browser-Based Authentication** – Uses Playwright to establish an authenticated session.
- **Data Transformation** – Cleans and normalizes raw API responses into Oracle-compatible records.
- **Oracle Database Integration** – Synchronizes data using SQL MERGE (UPSERT) operations.
- **Error Handling** – Handles authentication, API, and database connection errors.
- **Bulk Data Processing** – Supports efficient processing and synchronization of multiple Feature records.

---

## System Architecture

```text
+---------------+
|   ALM Octane  |
+-------+-------+
        |
        | REST API
        |
        v
+----------------------+
| Authentication Layer |
|     (Playwright)     |
+----------+-----------+
           |
           v
+----------------------+
|   Octane API Client  |
|    octane_api.py     |
+----------+-----------+
           |
           v
+----------------------+
| Transformation Layer |
|      parser.py       |
+----------+-----------+
           |
           v
+----------------------+
|  Oracle Persistence  |
|  save_to_oracle.py   |
+----------+-----------+
           |
           v
+----------------------+
|    OCTANE_FEATURES   |
|     Oracle Table     |
+----------------------+
```

---

## Data Synchronization Workflow

The integration process consists of four main stages.

### 1. Authentication

The application uses Playwright to launch a Chromium browser for OpenText ALM Octane authentication.

1. The user manually signs in to Octane.
2. After successful login, the user returns to the terminal.
3. The application extracts the browser session cookies.
4. An authenticated Python Requests session is created.

```text
Login complete? Press Enter
```

### 2. Data Extraction

The application retrieves Feature records using the Octane REST API.

**API Endpoint:**

```http
GET /api/shared_spaces/{space_id}/workspaces/{workspace_id}/features
```

The requested Feature attributes are maintained in `fields.py`.

The API response is returned in JSON format.

### 3. Data Transformation

The raw API response is processed and normalized into Oracle-compatible records.

| Transformation | Description |
|---|---|
| HTML Removal | Removes HTML tags from text descriptions |
| Date Conversion | Converts Octane timestamps into Python datetime objects |
| User Extraction | Extracts user names from nested API objects |
| Collection Flattening | Converts collections into semicolon-separated values |
| JSON Serialization | Converts dictionaries and arrays into JSON strings |
| Null Handling | Standardizes missing or empty values |

### 4. Oracle Database Synchronization

The transformed records are synchronized into Oracle using SQL `MERGE` statements.

The synchronization process supports:

- Updating existing Feature records.
- Inserting new Feature records.
- Committing transactions upon successful execution.
- Rolling back transactions when database errors occur.

---

## Project Structure

```text
octane-oracle-feature-integration/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
│
├── auth.py
├── config.py
├── fields.py
├── main.py
├── octane_api.py
├── oracle_db.py
├── parser.py
├── save_to_oracle.py
│
└── README.md
```

## Module Description

| Module | Responsibility |
|---|---|
| `main.py` | Application entry point that coordinates the synchronization workflow |
| `auth.py` | Handles browser-based authentication and session cookie extraction |
| `config.py` | Loads environment variables and application configurations |
| `fields.py` | Defines the Feature attributes retrieved from Octane |
| `octane_api.py` | Handles REST API requests and retrieves Feature data |
| `oracle_db.py` | Manages Oracle database connections |
| `parser.py` | Transforms raw API responses into Oracle-compatible records |
| `save_to_oracle.py` | Performs bulk data insertion and updates using MERGE statements |

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| OpenText ALM Octane | Source system for Feature data |
| REST API | Data retrieval and communication |
| Playwright | Browser-based authentication |
| Requests | HTTP requests and session management |
| BeautifulSoup4 | HTML content parsing and cleanup |
| Oracle Database | Target database for synchronized data |
| python-oracledb | Oracle database connectivity |
| python-dotenv | Environment variable management |

---

## Configuration

Create a `.env` file in the project root directory.

**Example configuration:**

```env
# Octane Configuration
BASE_URL=https://xxxxx
SHARED_SPACE_ID=xxxx
WORKSPACE_ID=xxxx

# Authentication Headers
XSRF-HEADER=xxxx
HPECLIENTTYPE=xxxx

# Oracle Database Configuration
ORACLE_USER=username
ORACLE_PASSWORD=password
ORACLE_HOST=hostname
ORACLE_PORT=portnumber
ORACLE_SERVICE=service_name
```

**Important:**

- Keep sensitive credentials in the `.env` file.
- Never commit the actual `.env` file to GitHub.
- Use `.env.example` as a template for environment configuration.

---

## Installation

### Prerequisites

- Python 3.10 or above.
- Access to OpenText ALM Octane.
- Access to Oracle Database.
- Required network or VPN connectivity.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd octane-oracle-feature-integration
```

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Chromium

```bash
playwright install chromium
```

### 5. Configure Environment Variables

Create a `.env` file based on `.env.example` and provide the required Octane and Oracle configuration values.

---

## Running the Application

Execute the following command from the project root directory:

```bash
python main.py
```

### Execution Steps

1. The application launches the Chromium browser.
2. Sign in to OpenText ALM Octane.
3. Return to the terminal.
4. Press Enter to continue.
5. The application retrieves Feature records through the REST API.
6. The retrieved data is transformed into Oracle-compatible records.
7. The records are synchronized into the Oracle database.

---

## Sample Execution Log

```text
============================================================
START OCTANE FEATURE SYNC
============================================================

Getting Feature Data From Octane API

Status Code: 200

Total Features: 100

Parsed Records: 100

Successfully saved 100 records into Oracle.

============================================================
OCTANE FEATURE SYNC COMPLETED
============================================================
```

---

## Oracle Database Synchronization

**Target Table:**

```sql
OCTANE_FEATURES
```

**Operation Type:**

```sql
MERGE (UPSERT)
```

**Primary Matching Condition:**

```sql
tgt.id = src.id
```

The Oracle `MERGE` operation performs the following:

- Updates existing records when a matching Feature ID is found.
- Inserts new records when no matching Feature ID exists.
- Maintains synchronized Feature information between Octane and Oracle.

---

## Error Handling

| Error Type | Possible Causes |
|---|---|
| Authentication | Incomplete login, expired session cookies, invalid XSRF header |
| API Connection | Incorrect Base URL, network issues, unavailable API |
| Oracle Connection | Invalid credentials, database unavailable, firewall restrictions |
| Database Merge | Invalid data, constraint violations, SQL execution errors |

The application uses exception handling and transaction rollback to manage database failures and prevent incomplete transactions.

---

## Project Purpose

This project demonstrates the integration of enterprise systems through REST APIs and Oracle Database.

It automates Feature data extraction, transformation, and synchronization, reducing manual data collection while providing a structured data source for enterprise reporting and analytics.