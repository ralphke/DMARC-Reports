# Copilot Instructions for DMARC-Reports

## Primary objective in this repository

Use Copilot to support the **full DMARC-to-Power BI/Fabric SDLC**: data ingestion, normalization, semantic modeling, DAX, report implementation, validation, and deployment/refresh operations.

When Power BI/Fabric work is requested, prioritize the **registered Microsoft MCP servers** for workspace/model/report operations instead of producing documentation-only output.

## Build, test, and lint commands

This repository is Python-script based (no dedicated build system).

```powershell
# Environment setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

```powershell
# Ingestion stage (Graph mailbox -> raw DMARC files)
python mailbox_fetch.py

# Normalization stage (raw DMARC -> partitioned CSV for BI)
python dmarc_parse.py
```

There is no configured automated test/lint framework in this repo (`pytest`, `tox`, `ruff`, `flake8`, `mypy`, etc. are not configured).

Single-run validation command for a targeted parse sample:

```powershell
python -c "from pathlib import Path; import dmarc_parse as p; f=next(Path('inbox').glob('**/*.xml')); df=p.sniff_and_parse_file(f); print(f'{f} -> {len(df)} rows')"
```

## End-to-end SDLC workflow for Power BI in Fabric (use MCP servers)

1. **Scope and requirements intake**
   - Start from repository sources: `PowerBI DMARC Report requirements.md`, `PowerBI_Dashboard_Specifications.md`, `PowerBI_DAX_Measures.md`, `PowerBI_Build_Guide.md`, and `README.md`.
   - Treat these files as the baseline contract for KPIs, page design, and metric semantics.

2. **Data acquisition (operational source)**
   - Use `mailbox_fetch.py` to pull DMARC attachments from Microsoft Graph with credentials in `.env`.
   - Keep `processed_messages.json` behavior intact for deduplicated incremental ingestion.

3. **Data normalization**
   - Use `dmarc_parse.py` to parse XML/ZIP/GZIP DMARC reports into normalized CSV outputs in `data_dmarc\`.
   - Preserve output partitioning by `report_end_utc` date (`dmarc_YYYY-MM-DD.csv`) because downstream BI guidance assumes this pattern.

4. **Fabric semantic model implementation (MCP-first)**
   - Use registered Microsoft MCP servers to create/update dataset/model assets in Fabric/Power BI workspace.
   - Map normalized fields directly to model columns; preserve boolean semantics of `dmarc_pass` and `both_fail`.
   - Keep a dedicated measures area/table pattern consistent with `PowerBI_DAX_Measures.md`.

5. **DAX implementation**
   - Implement measures from `PowerBI_DAX_Measures.md` before visual assembly.
   - Keep metric naming stable (for example: `DMARC Pass Rate`, `DKIM Pass Rate`, `SPF Pass Rate`, `Failed Auth Count`, `Spoofing Attempts`).
   - Do not rename base columns without updating all dependent measures and report visuals.

6. **Report build and UX**
   - Implement report pages/visuals according to `PowerBI_Dashboard_Specifications.md` and `PowerBI_Build_Guide.md`.
   - Preserve page intent: executive KPI summary, authentication analysis, threat monitoring, data quality, and trend analysis.

7. **Validation and release readiness**
   - Validate row/metric consistency between CSV source, model aggregations, and visuals.
   - Ensure filters/slicers interact correctly across required pages.
   - Confirm scheduled refresh assumptions align with ingestion timing (`mailbox_fetch.py` + `dmarc_parse.py` cadence).

8. **Deployment and operations in Fabric (MCP-first)**
   - Use registered Microsoft MCP servers for publish/update actions in Fabric workspace.
   - Keep operational documentation in sync with any model/report changes that alter field names, measure names, or page structure.

## Architecture context Copilot must preserve

- Pipeline shape is **Mailbox -> `inbox\YYYY\` -> parser -> `data_dmarc\dmarc_YYYY-MM-DD.csv` -> Power BI/Fabric model/report**.
- `mailbox_fetch.py` downloads only `.zip`, `.gz`, `.xml` attachments and tracks processed message IDs in `processed_messages.json`.
- `dmarc_parse.py` handles ZIP/GZIP/XML, normalizes DMARC record fields, computes `dmarc_pass` and `both_fail`, and writes date-partitioned CSV output.

## Repository-specific conventions

- Treat parser output schema as a contract for BI artifacts (especially `message_count`, `disposition`, `dkim_aligned`, `spf_aligned`, `dmarc_pass`, `both_fail`, `report_org`, `report_id`, `source_ip`).
- Preserve ingestion idempotency rules tied to `processed_messages.json`; do not bypass dedupe logic when changing mailbox ingestion.
- Keep extension filtering in fetch logic (`.zip`, `.gz`, `.xml`) aligned with parser format handling.
- Follow repository security workflow in `security.md`: no direct pushes to `main`; use feature branches and PR-based changes.

## Working rules for future Copilot sessions in this repo

- For Power BI/Fabric tasks, do real implementation steps through the registered Microsoft MCP servers where available (not only static markdown proposals).
- If a change impacts data schema, measures, or report page definitions, update all connected artifacts (parser output assumptions, DAX docs, and dashboard specification docs) in the same task.
- Keep guidance and changes aligned with existing repository documents; extend them rather than introducing parallel, conflicting instructions.
- For new dashboard requests that should follow the same pattern as the existing DMARC reports, start with the intake workflow in `PowerBI_Copilot_Intake_Guide.md` and use it to ask the user the minimum set of clarifying questions before generating requirements, specifications, DAX measures, and build guidance.

## Recommended MCP server baseline

Use this baseline for new environments and future Copilot sessions.

1. **Microsoft Power BI / Fabric MCP** (critical)
   - Use for semantic model creation/updates, DAX measure implementation, report edits, workspace deployment, and refresh operations.
   - Treat this as the default MCP for all model/report SDLC steps after CSV generation.

2. **Microsoft Graph MCP** (high)
   - Use for mailbox/message/attachment diagnostics and API-side validation that supports `mailbox_fetch.py`.
   - Use when ingestion fails, attachment counts drift, or mailbox query behavior needs investigation.

3. **Microsoft Entra ID MCP** (high)
   - Use for app registration, permissions/consent checks, and auth troubleshooting for Graph client credentials.
   - Use when token acquisition or permission scope issues block ingestion.

4. **Microsoft 365 / Outlook MCP** (medium, if available)
   - Use for operational mailbox checks (folder state, delivery behavior, message availability) that affect DMARC report intake.

### MCP usage by SDLC phase

- **Ingestion setup and troubleshooting**: Graph MCP + Entra ID MCP (+ Outlook MCP when mailbox behavior is unclear).
- **Modeling, DAX, report build, deployment**: Power BI / Fabric MCP first.
- **Release/operations**: Power BI / Fabric MCP for refresh and workspace updates; Graph/Entra MCP when data supply issues originate upstream.
