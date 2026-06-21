# Power BI DAX Measures for DMARC Reports

Copy and paste these measures into your Power BI model. Create a new table called `Measures` and add these as calculated measures.

## KPI Measures

### Overall DMARC Pass Rate
```dax
DMARC Pass Rate = 
DIVIDE(
    CALCULATE(SUM('DMARC Data'[message_count]), 'DMARC Data'[dmarc_pass] = TRUE()),
    SUM('DMARC Data'[message_count]),
    0
)
```

### DKIM Pass Rate
```dax
DKIM Pass Rate = 
DIVIDE(
    CALCULATE(SUM('DMARC Data'[message_count]), 'DMARC Data'[dkim_aligned] = "pass"),
    SUM('DMARC Data'[message_count]),
    0
)
```

### SPF Pass Rate
```dax
SPF Pass Rate = 
DIVIDE(
    CALCULATE(SUM('DMARC Data'[message_count]), 'DMARC Data'[spf_aligned] = "pass"),
    SUM('DMARC Data'[message_count]),
    0
)
```

### Both Fail Rate
```dax
Both Fail Rate = 
DIVIDE(
    CALCULATE(SUM('DMARC Data'[message_count]), 'DMARC Data'[both_fail] = TRUE()),
    SUM('DMARC Data'[message_count]),
    0
)
```

### Total Messages
```dax
Total Messages = SUM('DMARC Data'[message_count])
```

### Messages Rejected
```dax
Messages Rejected = 
CALCULATE(
    SUM('DMARC Data'[message_count]), 
    'DMARC Data'[disposition] = "reject"
)
```

### Messages Quarantined
```dax
Messages Quarantined = 
CALCULATE(
    SUM('DMARC Data'[message_count]), 
    'DMARC Data'[disposition] = "quarantine"
)
```

### Messages Passed
```dax
Messages Passed = 
CALCULATE(
    SUM('DMARC Data'[message_count]), 
    'DMARC Data'[disposition] = "none"
)
```

## Alignment Metrics

### DKIM & SPF Aligned
```dax
DKIM and SPF Aligned = 
DIVIDE(
    CALCULATE(
        SUM('DMARC Data'[message_count]), 
        'DMARC Data'[dkim_aligned] = "pass",
        'DMARC Data'[spf_aligned] = "pass"
    ),
    SUM('DMARC Data'[message_count]),
    0
)
```

### Either DKIM or SPF Aligned
```dax
Either DKIM or SPF Aligned = 
DIVIDE(
    CALCULATE(
        SUM('DMARC Data'[message_count]), 
        OR('DMARC Data'[dkim_aligned] = "pass", 'DMARC Data'[spf_aligned] = "pass")
    ),
    SUM('DMARC Data'[message_count]),
    0
)
```

### Neither DKIM nor SPF Aligned
```dax
Neither Aligned = 
DIVIDE(
    CALCULATE(
        SUM('DMARC Data'[message_count]), 
        'DMARC Data'[dkim_aligned] = "fail",
        'DMARC Data'[spf_aligned] = "fail"
    ),
    SUM('DMARC Data'[message_count]),
    0
)
```

## Security Metrics

### Spoofing Attempts (Header vs Envelope Mismatch)
```dax
Spoofing Attempts = 
CALCULATE(
    SUM('DMARC Data'[message_count]), 
    'DMARC Data'[header_from] <> 'DMARC Data'[envelope_from]
)
```

### Failed Authentication Count
```dax
Failed Auth Count = 
CALCULATE(
    SUM('DMARC Data'[message_count]), 
    'DMARC Data'[both_fail] = TRUE()
)
```

### Policy Enforcement Rate
```dax
Policy Enforcement Rate = 
DIVIDE(
    CALCULATE(
        SUM('DMARC Data'[message_count]), 
        OR('DMARC Data'[disposition] = "reject", 'DMARC Data'[disposition] = "quarantine")
    ),
    SUM('DMARC Data'[message_count]),
    0
)
```

## Trend Measures

### Messages by Disposition
```dax
Disposition Count = 
SWITCH(
    SELECTEDVALUE('DMARC Data'[disposition]),
    "none", 
        CALCULATE(SUM('DMARC Data'[message_count]), 'DMARC Data'[disposition] = "none"),
    "quarantine", 
        CALCULATE(SUM('DMARC Data'[message_count]), 'DMARC Data'[disposition] = "quarantine"),
    "reject", 
        CALCULATE(SUM('DMARC Data'[message_count]), 'DMARC Data'[disposition] = "reject"),
    BLANK()
)
```

## Data Quality Measures

### Reports Received
```dax
Reports Count = DISTINCTCOUNT('DMARC Data'[report_id])
```

### Organizations Reporting
```dax
Organizations Count = DISTINCTCOUNT('DMARC Data'[report_org])
```

### Unique Source IPs
```dax
Unique IPs = DISTINCTCOUNT('DMARC Data'[source_ip])
```

### Unique Sending Domains
```dax
Unique Domains = DISTINCTCOUNT('DMARC Data'[policy_domain])
```

## Formatting Tips

- **Pass Rates (%)**: Format as Percentage with 2 decimal places
- **Counts**: Format as Whole Number with thousands separator
- **Dates**: Format as Short Date
- **KPI Cards**: Use conditional formatting with green (>80%), yellow (50-80%), red (<50%)
