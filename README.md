# DMARC Reports

This repository collects DMARC aggregate report attachments from an Exchange mailbox, normalizes them into CSV files, and supports a Power BI dashboard for monitoring DMARC authentication and email security.

> The markdown documentation in this repo was created by Ralph Kemperdick with the help of GitHub Copilot.

## What this repo contains

- `mailbox_fetch.py` - fetches DMARC report attachments from an Exchange mailbox using Microsoft Graph API and saves them into `inbox/`.
- `dmarc_parse.py` - parses DMARC XML, ZIP, and GZIP files from `inbox/` and writes normalized CSV files to `data_dmarc/`.
- `data_dmarc/` - output directory containing generated `dmarc_YYYY-MM-DD.csv` files for Power BI.
- `inbox/` - raw DMARC report attachment files organized by year.
- `processed_messages.json` - tracks message IDs that have already been processed by `mailbox_fetch.py`.
- `requirements.txt` - Python dependencies used by the scripts.
- `PowerBI DMARC Report requirements.md` - business requirements for the Power BI dashboard.
- `PowerBI_Build_Guide.md` - step-by-step Power BI build instructions.
- `PowerBI_Dashboard_Specifications.md` - dashboard page and visual design details.
- `PowerBI_DAX_Measures.md` - recommended DAX measures for dashboard metrics.
- `PowerBI_Copilot_Intake_Guide.md` - reusable intake workflow for starting new Power BI/Fabric dashboard projects from this repository pattern.

## What the Python code does

### `mailbox_fetch.py`

This script:

- reads Azure app credentials from `.env`
- authenticates with Microsoft Graph API using MSAL
- queries a mailbox for messages containing attachments
- downloads `.zip`, `.gz`, and `.xml` DMARC report files
- saves them into `inbox/<year>/`
- updates `processed_messages.json` so messages are not reprocessed

### `dmarc_parse.py`

This script:

- scans `inbox/` recursively for DMARC report files
- supports ZIP archives, GZIP-compressed XML, and plain XML files
- parses DMARC report metadata, policy data, authentication results, and row counts
- normalizes each report into a pandas DataFrame
- writes one CSV file per report end date into `data_dmarc/`
- adds helper flags such as `dmarc_pass` and `both_fail`

## What the Power BI dashboard provides

The Power BI dashboard is designed to provide:

- DMARC pass/fail rates for DKIM, SPF, and overall authentication
- message disposition insights (`none`, `quarantine`, `reject`)
- failed authentication trends over time
- top source IPs and organizations producing failures
- spoofing and alignment issue detection
- policy enforcement and data quality metrics

The dashboard files and design notes include:

- how to load `data_dmarc/*.csv` into Power BI
- data type recommendations for message counts, dates, and boolean fields
- suggested measures for pass rate, total messages, failed counts, and spoofing metrics
- page layouts for executive summary, authentication analysis, threat detection, and monitoring

## Recreate the Power BI dashboard with Copilot

To recreate this Power BI dashboard using GitHub Copilot, use the Copilot plan mode first to define the dashboard scope and then switch to agent mode to implement the solution.

1. Use Copilot **plan mode** to generate a dashboard plan:
   - Describe the data sources, desired visuals, and the reporting pages you want.
   - Ask Copilot to create a step-by-step implementation plan for a DMARC dashboard built from `data_dmarc/*.csv`.
   - Include requirements such as KPI cards, authentication analysis, failure trends, and data quality monitoring.
   - Reference the existing markdown files in this repo (`PowerBI DMARC Report requirements.md`, `PowerBI_Build_Guide.md`, `PowerBI_Dashboard_Specifications.md`, `PowerBI_DAX_Measures.md`) so Copilot can align the new dashboard to current design and documentation.

2. Use Copilot **agent mode** to implement the plan:
   - Provide the implementation plan and the repository context.
   - Ask the agent to create or update Power BI documentation and markdown files as needed.
   - Use the agent to generate report structure, measure names, and Power BI build instructions.
   - If you want to preserve or extend the current documentation, ask Copilot to update the existing markdown files rather than creating separate copies.

3. Create and use the existing markdown files with Copilot:
   - In plan mode, ask Copilot to review the current markdown files and identify any gaps or missing dashboard details.
   - Ask Copilot to generate or refresh `PowerBI_Build_Guide.md`, `PowerBI_Dashboard_Specifications.md`, and `PowerBI_DAX_Measures.md` from the plan.
   - In agent mode, ask for a concrete implementation of those markdown files and how they map to the actual Power BI report pages.
   - For a new dashboard use case, start with `PowerBI_Copilot_Intake_Guide.md` so Copilot asks the right questions and produces the right artifacts.
   - You can also request Copilot to create a new markdown file that summarizes the dashboard architecture and data model.

### Important

- The Power BI MCP service is essential for best results when using Copilot to build or recreate this dashboard. It enables better Power BI-specific guidance, DAX creation, and report scaffolding.
- Without the Power BI MCP service, Copilot can still help, but the dashboard planning and implementation will be less tailored to Power BI features.

## Setup and installation

- Create and activate a Python virtual environment in the repo folder.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- Install dependencies.

```powershell
python -m pip install -r requirements.txt
```

- Create a `.env` file in the repo root with the following values:

```ini
TENANT_ID=your-tenant-id
CLIENT_ID=your-application-client-id
CLIENT_SECRET=your-client-secret
MAILBOX_UPN=mailbox@yourdomain.com
```

- Run the mailbox fetch script to download DMARC report attachments.

```powershell
python mailbox_fetch.py
```

- Run the parser to generate normalized CSVs for Power BI.

```powershell
python dmarc_parse.py
```

- Open Power BI Desktop and load the CSV files from `data_dmarc/`.

## Using a different credentials or context

If you want to run this repository in a different Azure tenant, mailbox, or environment:

- update the values in `.env` for the new tenant and mailbox
- use a registered Azure AD app with Graph API permissions for mailbox access
- set `MAILBOX_UPN` to the target mailbox user principal name
- ensure `CLIENT_ID` and `CLIENT_SECRET` belong to an app authorized for the tenant
- if the mailbox is different, the script will download attachments to the same `inbox/` structure
- if your DMARC reports arrive in a different file structure, place the raw files under `inbox/` or its year subfolders

### Notes for a different Power BI context

- change the folder path in Power BI if the repo location differs
- use the wildcard folder import pattern when loading `data_dmarc/*.csv`
- update the date table range and relationships for the new dataset
- verify the Power BI measures in `PowerBI_DAX_Measures.md` match your naming conventions

## Tips

- Keep `processed_messages.json` with the mailbox fetch script to avoid duplicate downloads.
- Keep `data_dmarc/` under source control only if you want versioned snapshot CSVs; otherwise, regenerate it from `inbox/`.
- Review `PowerBI_Build_Guide.md` and `PowerBI_Dashboard_Specifications.md` before creating visuals.

## Glossary

- `DMARC`: Domain-based Message Authentication, Reporting & Conformance
- `DKIM`: DomainKeys Identified Mail
- `SPF`: Sender Policy Framework
- `dmarc_pass`: true if DKIM or SPF passed for the message row
- `both_fail`: true if both DKIM and SPF failed

## Support

If you need to adapt the repository to a new tenant or email host, update `.env`, re-run the fetch and parser scripts, and then refresh your Power BI dataset.
