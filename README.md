# SonarQube Bug Export Workaround

The Community Edition of SonarQube does not provide an official way to **export unresolved issues** or **generate bug reports**. This project offers a **workaround** by programmatically retrieving and correlating SonarQube issues with their rule metadata, producing a useful `.csv` export.


##  Features

- ✅ Export **unresolved issues** from any project analyzed by SonarQube.
- ✅ Enrich issues with **rule metadata** (bug descriptions, language, etc.).
- ✅ Generate a clean, de-duplicated `bug_fixes.csv` file.
- ✅ Fully automated with Python and SonarQube REST APIs.

##  How It Works

This tool leverages **SonarQube's REST API** to extract project-specific issues and metadata. Here's the flow:

1. **Rule Metadata Collection** (`all_rules_scraping.py`):
   - Authenticates using your API token.
   - Calls the `/api/rules/search` endpoint.
   - Iterates through all pages and extracts rule key, language, and description.
   - Saves to `all_sonarqube_rules.csv`.

2. **Unresolved Issue Extraction** (`repo_rules_scraping.py`):
   - Prompts the user to input a SonarQube project key.
   - Calls the `/api/issues/search` endpoint with filters for unresolved issues.
   - Extracts rule key and filename from each issue.
   - Saves raw output to `unresolved_issues.csv`.

3. **Merging & Enrichment**:
   - Loads both CSV files using `pandas`.
   - Merges them on the rule key (`key` ↔ `rule`) to enrich issues with rule info.
   - Selects and renames columns: `code_language`, `file_name`, and `bug_description`.
   - Removes duplicates and saves final `bug_fixes.csv`.

 **Final Output:** A clean list of file-level issues enriched with descriptions for bug tracking, analysis, or automation.


## Pre-requisites

- ✅ Python 3.7+
- ✅ SonarQube Community Edition (running at `http://localhost:9000`)
- ✅ A valid **SonarQube API Token**
- ✅ Installed Python packages:
  - `requests`
  - `pandas`

You can install dependencies via:

```bash
pip install -r requirements.txt
```

_If `requirements.txt` is missing:_

```bash
pip install requests pandas
```

## Installation

1. Clone this repository or download the scripts:

```bash
git clone https://github.com/your-username/sonarqube-export-workaround.git
cd sonarqube-export-workaround
```

2. Ensure SonarQube server is running:

```bash
docker ps
# Look for container with name like 'sonarqube' and port 9000 exposed
```

3. Replace the `TOKEN` in both Python files with your **SonarQube API token**:

```python
TOKEN = "your_actual_sonar_token_here"
```

## Usage

There are **two main steps**:

### Step 1: Download All SonarQube Rules

This script pulls metadata for all rules:

```bash
python3 all_rules_scraping.py
```

Output:
- `all_sonarqube_rules.csv`

### Step 2: Export Unresolved Issues for a Project

```bash
python3 repo_rules_scraping.py
```

It will prompt:

```
enter the repo for which u want to pull the bugs :
```

 Provide your project key (e.g., `my_project_key`)

Output:
- `unresolved_issues.csv`
- `bug_fixes.csv` (final enriched file)


## Example Session

```bash
$ python3 all_rules_scraping.py
 Fetching page 1...
 Fetching page 2...
...
 Saved 4023 rules to 'all_sonarqube_rules.csv'

$ python3 repo_rules_scraping.py
enter the repo for which u want to pull the bugs : my_project_key
df1: Index(['key', 'repo', 'name'], dtype='object')
df2: Index(['rule', 'file_name'], dtype='object')
Merge completed. Saved to bug_fixes.csv
```

Final `bug_fixes.csv` will look like:

| code_language | file_name       | bug_description                     |
|---------------|------------------|--------------------------------------|
| java          | MyClass.java     | “Equals() should not be used...”     |
| py            | script.py        | “Use ‘is’ for comparison to None...” |

This workaround gives SonarQube Community users better visibility into issues and supports external analysis or automation.

## Demo Video
https://github.com/user-attachments/assets/d5d4a224-895d-4114-8b83-49424017ab57



