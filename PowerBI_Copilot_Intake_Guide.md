# Power BI/Fabric Dashboard Intake Guide

Use this guide when a new dashboard project should start from this repository pattern. The goal is to help the user provide the minimum set of answers that let Copilot create the same kinds of artifacts used for the current DMARC dashboard.

## What Copilot should capture first

Before creating or updating Power BI artifacts, Copilot should ask the user for the following information:

1. Business objective
   - What decision, monitoring need, or operational question should the dashboard answer?
   - Who is the primary audience for the report?

2. Data source context
   - What system or file source provides the data?
   - What tables, columns, or fields are expected?
   - What refresh cadence or update frequency is required?

3. Dashboard scope
   - Which pages should the report contain?
   - Which KPI cards, charts, tables, and filters are required?
   - Should the report support drill-through, bookmarks, or cross-page filtering?

4. Measure definitions
   - Which metrics must be shown?
   - How should success, failure, trend, or rate metrics be calculated?
   - Are there existing naming conventions or business definitions to preserve?

5. Delivery and deployment expectations
   - Is the target Power BI Service, Fabric workspace, or a local Power BI Desktop file?
   - Are there security, sensitivity, or access constraints?
   - Does the report need scheduled refresh or deployment automation?

6. Visual and branding constraints
   - What colors, layout, page order, or style should be used?
   - Are there accessibility or readability requirements?

## Suggested intake template

Copilot can use the following template to guide the conversation:

- Dashboard purpose:
- Primary audience:
- Source data system:
- Expected data shape or schema:
- Required pages:
- Required visuals:
- Required measures/KPIs:
- Filters/slicers:
- Deployment target:
- Refresh cadence:
- Branding or formatting constraints:

## Expected output after the intake completes

Once the user answers the intake questions, Copilot should create or update the repository artifacts that match the DMARC workflow:

1. Requirements document
2. Dashboard specifications document
3. DAX measures document
4. Build guide
5. Optional implementation notes for data model and deployment

## Recommended starter prompt

Use this prompt when starting a new dashboard request:

"Help me define a new Power BI dashboard for [use case]. Use this repository as the starting point, ask me the minimum set of questions needed to create the requirements, dashboard specifications, DAX measures, and build guide, and then generate those artifacts for me."
