# Power BI DMARC Dashboard - Build Guide

## Step 1: Prepare Your Data in Power BI Desktop

### Load the Data
1. Open **Power BI Desktop**
2. Click **Home** → **Get Data** → **Text/CSV**
3. Navigate to your `data_dmarc` folder
4. Select one CSV file first (e.g., `dmarc_2026-01-03.csv`)
5. Click **Load**
6. In the query editor, change **Source** to use a wildcard:
   - In the **Advanced Editor**, modify the path to: `"c:\Users\RalphKemperdick\OneDrive - RaKeTe-Technology\DMARC-Reports\data_dmarc\*.csv"`
   - This will combine all CSV files automatically
7. Click **Close & Apply**

### Transform Data Types
In **Power Query Editor**:
- `message_count` → **Whole Number**
- `report_begin_utc`, `report_end_utc` → **Date/Time**
- `dmarc_pass`, `both_fail` → **True/False**
- All text fields → **Text**

## Step 2: Create the Data Model

1. Switch to **Model** view
2. Rename the table to `DMARC Data`
3. Create a **Date Table** (recommended):
   - Click **New Table**
   - Paste this formula:
   ```dax
   Dates = CALENDAR(DATE(2025,1,1), TODAY())
   ```
4. Create relationships:
   - Link `DMARC Data[report_date]` → `Dates[Date]`

## Step 3: Add DAX Measures

1. In **Model** view, create a new table:
   - Click **New Table**
   - Name it `Measures`
   - Delete the auto-generated column
2. Copy all measures from `PowerBI_DAX_Measures.md`
3. Paste them into the `Measures` table using **New Measure**

## Step 4: Build Dashboard Pages

### Page 1: Executive Summary (KPIs & Trends)

**Layout:** 3 rows, adjust as needed

#### Row 1: KPI Cards
Create **4 cards** using **Card visual**:
- **Card 1:** DMARC Pass Rate
  - Drag `Measures[DMARC Pass Rate]` to Values
  - Format: Percentage, 0 decimals
  - Add conditional formatting: Green ≥80%, Yellow 50-80%, Red <50%

- **Card 2:** DKIM Pass Rate
  - Format same as above

- **Card 3:** SPF Pass Rate
  - Format same as above

- **Card 4:** Total Messages
  - Drag `Measures[Total Messages]` to Values
  - Format: Whole Number with thousands separator

#### Row 2: Message Disposition Pie Chart
- Visual: **Pie Chart**
- Values: `Measures[Total Messages]` (sum)
- Legend: `DMARC Data[disposition]`
- Data labels: Show percentages
- Color code: Green=none, Yellow=quarantine, Red=reject

#### Row 3: Daily Message Trend
- Visual: **Line Chart**
- X-axis: `Dates[Date]`
- Y-axis: `Measures[Total Messages]`
- Add legend for disposition breakdown (optional stacked area)

### Page 2: Authentication Analysis

**Layout:** 2x2 grid

#### Top-Left: Authentication Status Breakdown (Stacked Bar)
- Visual: **Stacked Column Chart**
- X-axis: `DMARC Data[policy_domain]`
- Y-axis: `Measures[Total Messages]`
- Legend: 
  - Add one column for "DKIM Pass"
  - Add one for "SPF Pass"
  - Add one for "Both Fail"
- Limit to top 15 domains

#### Top-Right: DKIM vs SPF Performance (Clustered Bar)
- Visual: **Clustered Bar Chart**
- Values: `Measures[DKIM Pass Rate]`, `Measures[SPF Pass Rate]`
- Add visual filters for top 10 reporting orgs

#### Bottom-Left: Alignment Rates (Gauge/KPI)
- Create 3 **Gauge** visuals:
  1. "DKIM & SPF Aligned" - Target: 100%
  2. "Either Aligned" - Target: 100%
  3. "Neither Aligned" - Target: 0%

#### Bottom-Right: Authentication Results Table
- Visual: **Table**
- Columns:
  - `DMARC Data[policy_domain]`
  - `DMARC Data[auth_dkim_result]`
  - `DMARC Data[auth_spf_result]`
  - `Measures[Total Messages]`
- Sort: By message count descending
- Conditional formatting on results (Green=pass, Red=fail)

### Page 3: Security & Threat Detection

**Layout:** 2x2 grid

#### Top-Left: Failed Authentication Sources (Top 20 IPs)
- Visual: **Horizontal Bar Chart**
- Values: `Measures[Failed Auth Count]`
- X-axis: `DMARC Data[source_ip]`
- Sort: Descending
- Data labels: Show values
- Limit to top 20

#### Top-Right: Failure Reason Distribution (Donut)
- Visual: **Donut Chart**
- Values: `Measures[Failed Auth Count]`
- Legend: `DMARC Data[fail_reason_type]`
- Data labels: Show category and percentage

#### Bottom-Left: Spoofing Attempts Trend
- Visual: **Line Chart**
- X-axis: `Dates[Date]`
- Y-axis: `Measures[Spoofing Attempts]`
- Add threshold line at 0 for reference
- Color: Red/Orange

#### Bottom-Right: Policy Enforcement Metrics (Cards)
Create 3 cards in a row:
- **Rejected:** `Measures[Messages Rejected]`
- **Quarantined:** `Measures[Messages Quarantined]`
- **Passed:** `Measures[Messages Passed]`
- Add percentage breakdown in descriptions

### Page 4: Data Quality & Monitoring

**Layout:** 1 row top, 1 row bottom

#### Top Row: Summary Metrics (5 Cards)
- Reports Received
- Organizations Reporting
- Unique IPs
- Unique Domains
- Date Range (Latest Report Date)

#### Bottom: Reporting Organizations Table
- Visual: **Table**
- Columns:
  - `DMARC Data[report_org]`
  - `DMARC Data[report_email]`
  - `Measures[Reports Count]`
  - `Measures[Total Messages]`
  - `Measures[DMARC Pass Rate]` (as %)
- Sort: By message count descending
- Conditional formatting on pass rate

### Page 5: Time Series & Trends

**Layout:** Full-width charts

#### Chart 1: Daily Trend by Disposition (100% Stacked Area)
- Visual: **Area Chart**
- X-axis: `Dates[Date]`
- Y-axis: `Measures[Total Messages]`
- Legend (stacked): `DMARC Data[disposition]`
- Select: "Show as percentage"

#### Chart 2: Weekly Rolling Pass Rate
- Visual: **Line & Clustered Column Chart**
- X-axis: `Dates[Date]`
- Line: `Measures[DMARC Pass Rate]`
- Columns: `Measures[Total Messages]`

#### Chart 3: Top Organizations Performance (Week over Week)
- Visual: **Matrix**
- Rows: `DMARC Data[report_org]`
- Columns: Week number or month
- Values: `Measures[DMARC Pass Rate]`
- Conditional formatting: Color scale (Red=low, Green=high)

## Step 5: Add Interactivity

### Slicers (Add to all relevant pages)
1. **Date Slicer**
   - Drag `Dates[Date]` to a new Slicer visual
   - Set to **Relative date** or **Between** range
   - Apply to all pages

2. **Domain Filter Slicer**
   - Drag `DMARC Data[policy_domain]`
   - Apply to pages 2, 3, 5

3. **Disposition Slicer**
   - Drag `DMARC Data[disposition]`
   - Apply to pages 1, 3

4. **Organization Slicer**
   - Drag `DMARC Data[report_org]`
   - Apply to pages 2, 4, 5

### Bookmarks (Navigation)
- Create bookmarks for each page view state
- Add buttons for "Reset Filters" and "Print View"

## Step 6: Formatting & Polish

### Theme & Colors
1. Click **View** → **Themes** → Choose a professional theme
2. Use consistent colors:
   - Green: #2ECC71 (Pass/Success)
   - Yellow: #F39C12 (Warning/Quarantine)
   - Red: #E74C3C (Failed/Reject)
   - Gray: #95A5A6 (Neutral)

### Page Titles
- Add **Text Box** at top of each page with title and description
- Font: 24pt, Bold, Dark Gray

### Tooltips
- Right-click any visual → **Tooltip**
- Customize to show relevant metrics on hover

### Mobile View
- Click **View** → **Mobile Layout**
- Resize visuals for mobile devices
- Test on different screen sizes

## Step 7: Publish & Schedule

1. Click **File** → **Publish**
2. Select your Power BI workspace
3. Configure data refresh:
   - **Workspace settings** → **Datasets**
   - Set to refresh daily after mailbox_fetch.py runs
4. Share with stakeholders
5. Set up **Row-Level Security (RLS)** if needed

## Step 8: Maintenance

### Weekly Tasks
- Check for data quality issues in the Data Quality page
- Review security alerts on the Threat Detection page
- Monitor organization performance trends

### Monthly Tasks
- Create snapshot reports for audit purposes
- Review overall DMARC posture improvements
- Share insights with security team

### Quarterly Tasks
- Adjust DMARC policies based on trend analysis
- Update organization contacts for high-failure senders
- Review and refine dashboard based on user feedback
