# Power BI DMARC Dashboard - Detailed Specifications

## Dashboard Overview

A comprehensive 5-page Power BI dashboard for monitoring DMARC authentication, security threats, and email compliance metrics.

---

## Page 1: Executive Summary

**Purpose:** High-level view of DMARC health and trends  
**Audience:** C-level executives, security managers

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  DMARC Authentication Dashboard - Executive Summary              │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────┬──────────┬──────────┬──────────────┐                │
│ │DMARC Pass│DKIM Pass │SPF Pass  │Total Messages│                │
│ │  85.2%   │  92.1%   │  88.5%   │  2,847,392   │                │
│ └──────────┴──────────┴──────────┴──────────────┘                │
├─────────────────────────────────────────────────────────────────┤
│  Disposition Breakdown          │  Daily Message Trend            │
│  ┌─────────────────────────┐    │  ┌──────────────────────────┐  │
│  │    ◐ Passed  (80%)      │    │  │ 300K                     │  │
│  │    ◑ Quarantined (12%)  │    │  │ 250K  ╱╲    ╱╲           │  │
│  │    ● Rejected  (8%)     │    │  │ 200K ╱  ╲╱  ╱  ╲╱╲       │  │
│  │                         │    │  │ 150K                    │  │
│  └─────────────────────────┘    │  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Visuals

1. **KPI Cards (Top Row)**
   - DMARC Pass Rate: Percentage, green/yellow/red conditional formatting
   - DKIM Pass Rate: Percentage
   - SPF Pass Rate: Percentage
   - Total Messages: Card with icon

2. **Disposition Pie Chart (Bottom Left)**
   - Size: 40% width
   - Shows split: none/quarantine/reject
   - Color-coded by disposition status
   - Data labels: Category % and count

3. **Daily Trend Line (Bottom Right)**
   - X-axis: Date (daily)
   - Y-axis: Message count (0-500K range)
   - Optional: Multiple lines for DKIM/SPF pass vs. fail
   - Trend indicators: Up/down arrows showing variance

### Filters
- Date range slicer (top left corner)
- Optional: Disposition filter

---

## Page 2: Authentication Analysis

**Purpose:** Deep dive into DKIM and SPF authentication performance  
**Audience:** Email/security engineers

### Layout

```
┌──────────────────────────────────────────────────────────────┐
│  Authentication Analysis                                      │
├──────────────────────────────────────────────────────────────┤
│ ┌────────────────────────────┬────────────────────────────┐  │
│ │Authentication Status       │ DKIM vs SPF Performance   │  │
│ │(Top Domains)               │ (Top Organizations)       │  │
│ │ ┌──────────────────────┐   │ ┌──────────────────────┐  │  │
│ │ │ Domain A   ▓▓▓▓▓    │   │ │ DKIM  SPF            │  │  │
│ │ │ Domain B   ▓▓▓▓     │   │ │ ████  ░░░░░          │  │  │
│ │ │ Domain C   ▓▓▓      │   │ │ ████  ░░░░           │  │  │
│ │ │ ...        ...      │   │ │ ...   ...            │  │  │
│ │ └──────────────────────┘   │ └──────────────────────┘  │  │
│ ├────────────────────────────┼────────────────────────────┤  │
│ │Alignment Gauges            │ Auth Results Table         │  │
│ │ DKIM & SPF:  ████░ 88%     │ ┌────┬───────┬────────┐   │  │
│ │ Either:      █████░ 94%    │ │Dom │DKIM  │SPF     │   │  │
│ │ Neither:     ░░░░░░░░░░ 6% │ │ A  │pass  │fail    │   │  │
│ │             (Target: 0%)   │ │ B  │pass  │pass    │   │  │
│ │                            │ │ C  │fail  │pass    │   │  │
│ │                            │ └────┴───────┴────────┘   │  │
│ └────────────────────────────┴────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Visuals

1. **Authentication Status Stacked Column Chart (Top Left)**
   - X-axis: Top 15 policy domains
   - Y-axis: Message count (0-1M)
   - Stacked by: DKIM pass, SPF pass, both fail
   - Color: Green (pass) / Red (fail)
   - Hover shows percentage breakdown

2. **DKIM vs SPF Performance Clustered Bar (Top Right)**
   - X-axis: Top 10 reporting organizations
   - Y-axis: Pass rate percentage (0-100%)
   - Two bars per org: DKIM rate vs. SPF rate
   - Data labels: Show percentages
   - Target line at 100%

3. **Alignment Metrics Gauges (Bottom Left)**
   - Three gauge visuals (vertically stacked)
   - Gauge 1: "DKIM & SPF Aligned" (Target: 100%)
   - Gauge 2: "Either Aligned" (Target: 100%)
   - Gauge 3: "Neither Aligned" (Target: 0%)
   - Color zones: Green ≥90%, Yellow 50-90%, Red <50%

4. **Authentication Results Table (Bottom Right)**
   - Columns: Domain | DKIM Result | SPF Result | Message Count | Pass Rate
   - Sort: By message count (descending)
   - Conditional formatting:
     - DKIM/SPF columns: Green=pass, Red=fail
     - Pass Rate: Color scale gradient
   - Limit to 20 rows (with scroll)

### Filters
- Date range slicer
- Organization name slicer
- Domain name slicer

---

## Page 3: Security & Threat Detection

**Purpose:** Identify suspicious activity and security risks  
**Audience:** Security analysts, incident response team

### Layout

```
┌──────────────────────────────────────────────────────────────┐
│  Security & Threat Detection                                  │
├──────────────────────────────────────────────────────────────┤
│ ┌────────────────────────┬────────────────────────────────┐  │
│ │Failed Auth Sources     │ Failure Reasons               │  │
│ │(Top 20 IPs)            │ (Distribution)                │  │
│ │ ┌──────────────────┐   │ ┌────────────────────────┐    │  │
│ │ │192.168.1.10  ▓░░░│   │ │    ◐ Misalignment     │    │  │
│ │ │10.0.0.50     ▓▓░░│   │ │    ◑ Missing DKIM     │    │  │
│ │ │8.8.8.8       ▓▓▓░│   │ │    ● Missing SPF      │    │  │
│ │ │...           ... │   │ │    ◕ Policy Reject    │    │  │
│ │ └──────────────────┘   │ └────────────────────────┘    │  │
│ ├────────────────────────┼────────────────────────────────┤  │
│ │Spoofing Attempts Trend │ Policy Enforcement Metrics    │  │
│ │ ┌──────────────────┐   │ ┌──────────┬───────┬────────┐ │  │
│ │ │ 5K               │   │ │Rejected: │Quaran:│Passed: │ │  │
│ │ │ 4K  ╱╲           │   │ │  125K    │250K   │2.5M    │ │  │
│ │ │ 3K ╱  ╲  ╱╲      │   │ │  (4.2%)  │(8.5%) │(87.3%)│ │  │
│ │ │ 2K               │   │ │          │       │        │ │  │
│ │ └──────────────────┘   │ └──────────┴───────┴────────┘ │  │
│ └────────────────────────┴────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Visuals

1. **Failed Authentication Sources Bar Chart (Top Left)**
   - Visual type: Horizontal bar chart
   - X-axis: Failed auth count (0-50K)
   - Y-axis: Source IP (top 20)
   - Color: Red gradient (darker = more failures)
   - Data labels: Show count values
   - Hover tooltip: IP, ASN, Country (if available)

2. **Failure Reason Distribution Donut (Top Right)**
   - Inner label: Total failures
   - Segments: fail_reason_type values
   - Colors: Different colors per reason
   - Data labels: Category name and percentage
   - Top 5 reasons highlighted

3. **Spoofing Attempts Trend Line (Bottom Left)**
   - X-axis: Date (daily)
   - Y-axis: Spoofing count (0-10K)
   - Line color: Orange/Red
   - Optional: Add reference line at 0
   - Trend annotation: Up/down indicators
   - Highlight anomalies on hover

4. **Policy Enforcement Cards (Bottom Right)**
   - Three large cards in a row:
     - **Card 1 - Rejected:** `[Messages Rejected]` count
       - Subtitle: Percentage of total
       - Icon: Alert/block icon
       - Color: Red
     - **Card 2 - Quarantined:** `[Messages Quarantined]` count
       - Subtitle: Percentage of total
       - Icon: Warning icon
       - Color: Yellow
     - **Card 3 - Passed:** `[Messages Passed]` count
       - Subtitle: Percentage of total
       - Icon: Check icon
       - Color: Green

### Filters
- Date range slicer
- Failure reason type slicer
- Source IP slicer (optional, limited to top 100)

---

## Page 4: Data Quality & Monitoring

**Purpose:** Verify data completeness and monitor system health  
**Audience:** Data stewards, IT operations

### Layout

```
┌──────────────────────────────────────────────────────────────┐
│  Data Quality & Monitoring                                    │
├──────────────────────────────────────────────────────────────┤
│ ┌───────┬────────┬──────────┬────────────┬──────────────┐    │
│ │Reports│Orgs    │Unique IPs│Unique Doms │Latest Report │   │
│ │Received│        │          │            │Date          │   │
│ │  243  │  18    │  8,247   │  127       │ Jan 17, 2026 │   │
│ └───────┴────────┴──────────┴────────────┴──────────────┘    │
├──────────────────────────────────────────────────────────────┤
│ Reporting Organizations & Performance                         │
│ ┌───────────────────┬──────┬─────────┬────────────┬────────┐ │
│ │Organization      │Reports│Messages │DMARC Rate │Status  │ │
│ │ report.org1      │  45   │ 1,250K  │  92.3%    │  ✓     │ │
│ │ report.org2      │  32   │  850K   │  78.5%    │  ⚠     │ │
│ │ report.org3      │  28   │  510K   │  65.2%    │  ⚠     │ │
│ │ report.org4      │  15   │  237K   │  99.1%    │  ✓     │ │
│ │ ...              │  ...  │  ...    │  ...      │  ...   │ │
│ └───────────────────┴──────┴─────────┴────────────┴────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### Visuals

1. **Summary KPI Cards (Top Row)**
   Five card visuals:
   - **Card 1:** Reports Received Count
   - **Card 2:** Organizations Reporting Count
   - **Card 3:** Unique Source IPs Count
   - **Card 4:** Unique Domains Count
   - **Card 5:** Latest Report Date
   
   Formatting: Large numbers, icons, subtle background colors

2. **Reporting Organizations Table (Bottom)**
   - Columns (in order):
     1. `report_org` - Organization name (text, sortable)
     2. `Reports Count` - DISTINCTCOUNT(report_id) (whole number)
     3. `Total Messages` - SUM(message_count) (whole number, formatted with K/M)
     4. `DMARC Pass Rate` - [DMARC Pass Rate] measure (percentage, 1 decimal)
     5. `Status` - Custom column (visual indicator: ✓/⚠/✗)
   
   - Sorting: Default by message count (descending)
   - Conditional formatting:
     - Pass Rate column: 
       - Green (≥90%): ✓
       - Yellow (70-89%): ⚠
       - Red (<70%): ✗
     - Message count: Subtle blue background gradient
   
   - Row count: 50 with scrolling
   - Pagination or dynamic filtering available

### Filters
- Date range slicer
- Organization name slicer (for drilling down)

---

## Page 5: Time Series & Trends

**Purpose:** Historical analysis and trend forecasting  
**Audience:** Analysis team, trend monitoring

### Layout

```
┌──────────────────────────────────────────────────────────────┐
│  Time Series & Trends Analysis                                │
├──────────────────────────────────────────────────────────────┤
│  Daily Disposition Trend (100% Stacked Area)                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 100% ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │ │
│  │      ░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░ │ │
│  │      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │ │
│  │  0%  └──────────────────────────────────────────────────┘ │
│  └──────────────────────────────────────────────────────────┘ │
│  Weekly Rolling Pass Rate vs Volume                           │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │100%║ ═════════════════════════════════════════════════ │ │
│  │    ║   ╱╲         ╱╲                                  │ │
│  │ 80%║  ╱  ╲  ╱╲  ╱  ╲  ╱╲                             │ │
│  │    ║ ╱    ╲╱  ╲╱    ╲╱  ╲                            │ │
│  │    ║┌─────────────────────────────────────────────┐  │ │
│  │    │ 500K Msgs ████  200K ████████                │  │ │
│  │    └─────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────┘ │
│  Top Organizations - Pass Rate Performance (Heat Map)       │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Organization      │ W1  │ W2  │ W3  │ W4  │ Monthly    │ │
│  │ report.org1       │95% │92% │94% │96% │ 94.3%       │ │
│  │ report.org2       │78% │81% │75% │82% │ 79.0%       │ │
│  │ report.org3       │64% │68% │71% │73% │ 69.0%       │ │
│  └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### Visuals

1. **Daily Disposition Trend 100% Stacked Area (Top)**
   - X-axis: Date (daily, with month markers)
   - Y-axis: 0-100% (percentage)
   - Series (stacked, bottom to top): none (green) → quarantine (yellow) → reject (red)
   - Trend visibility: Shows policy enforcement effectiveness
   - Hover: Shows absolute counts and percentages for each date

2. **Weekly Rolling Pass Rate vs Volume Combo Chart (Middle)**
   - Visual type: Line & Clustered Column
   - X-axis: Date (weekly buckets)
   - Left Y-axis: Pass rate percentage (0-100%)
   - Right Y-axis: Message volume (0-1M)
   - Line: `[DMARC Pass Rate]` - Color: Blue, Target at 85%
   - Columns: `[Total Messages]` - Color: Light gray
   - Data labels: Show weekly pass rate percentage

3. **Organization Performance Heat Map (Bottom)**
   - Visual type: Matrix
   - Rows: Top 15 organizations by message volume
   - Columns: Week number or calendar month
   - Values: `[DMARC Pass Rate]` formatted as percentage
   - Conditional formatting: Color scale
     - Green: 90-100%
     - Yellow: 70-89%
     - Orange: 50-69%
     - Red: <50%
   - Data labels: Show percentage in each cell
   - Tooltips: Include message count and trend direction

### Filters
- Date range slicer (with preset ranges: Last 7 days, Last 30 days, Last 90 days)
- Organization slicer
- Optional: Disposition filter

---

## Global Dashboard Features

### Navigation & Interaction

1. **Page Tabs**
   - Located at bottom of each page
   - Visual indicator of current page
   - Tooltips on hover showing page description

2. **Slicers (Consistent Across Pages)**
   - **Date Range Slicer** (Top-left of each page)
     - Type: Between dates or relative date
     - Default: Last 30 days
     - Applies to: All pages
   
   - **Domain Slicer** (Top-center where applicable)
     - Type: List or dropdown
     - Applies to: Pages 2, 3, 5
   
   - **Organization Slicer** (Top-right where applicable)
     - Type: List or dropdown
     - Applies to: Pages 2, 4, 5
   
   - **Disposition Slicer** (Where relevant)
     - Type: Buttons (none, quarantine, reject, all)
     - Applies to: Pages 1, 3

3. **Buttons & Actions**
   - Reset Filters button: Clears all slicers
   - Refresh Data button: Manual data refresh trigger
   - Print View button: Optimizes for printing
   - Help icon: Links to documentation

### Tooltips
- Every visual should have rich tooltips
- Include measure names and values
- Show trends (↑ up, ↓ down) for relevant metrics
- Date context shown in tooltips

### Color Scheme
- **Primary Colors:**
  - Success (Green): #2ECC71
  - Warning (Yellow): #F39C12
  - Alert (Red): #E74C3C
  - Neutral (Gray): #95A5A6
  
- **Accent Colors:**
  - Primary blue: #3498DB
  - Light gray: #ECF0F1
  - Dark gray: #34495E

### Typography
- Title font size: 24pt, Bold
- Section headers: 18pt, Semi-bold
- Card values: 36pt, Bold
- Default text: 11pt, Regular

### Performance Considerations
- Load top 100 entries for tables by default
- Aggregate data to daily level for trends
- Use field-level security for sensitive domains if needed
- Cache calculations where possible

---

## Success Metrics & KPIs

### Dashboard Health Targets
- DMARC Pass Rate: ≥85% (green), 70-84% (yellow), <70% (red)
- DKIM Pass Rate: ≥90%
- SPF Pass Rate: ≥85%
- Policy Enforcement: 100% (must take action on failures)
- Spoofing Attempts: Trending down month-over-month

### Data Quality Standards
- Report latency: <24 hours
- Data completeness: 99%+
- Unique organizations monitored: 10+
- Unique domains tracked: 50+
