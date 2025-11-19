# Contacts Management System

Professional contact database management with deduplication, classification, and Excel export capabilities.

## Overview
Processes multiple CSV files to create a unified contact database with intelligent business/personal classification, duplicate removal, and professional Excel export.

## Quick Start
1. Place CSV files in `input/` directory
2. Run `python process_contacts.py`
3. Review results in `output/contacts_master.xlsx`

## Features
- **Multi-CSV Processing:** Handles various CSV formats and encodings
- **Smart Deduplication:** Intelligent duplicate detection using multiple criteria
- **Business Classification:** Automatic business/personal categorization based on email domains
- **Data Quality Assurance:** Validation, cleaning, and accuracy verification
- **Professional Export:** Formatted Excel output with multiple worksheets
- **Privacy Protection:** Secure handling of personal information (PII)

## Input Files
Currently processing:
- contacts.csv
- contacts (1).csv
- contacts (2).csv
- contacts (3).csv
- contacts (4).csv

## Output Structure
- **contacts_master.xlsx** - Main output file with multiple sheets:
  - Contacts_Master: All deduplicated contacts
  - Business_Contacts: Business/professional contacts
  - Personal_Contacts: Personal/individual contacts
  - Data_Quality_Report: Processing statistics and issues
  - Processing_Log: Audit trail

## Contact Classification
- **Business:** Corporate domains, work emails, professional services
- **Personal:** Gmail, Yahoo, personal domains, individual contacts
- **Other:** Unknown or ambiguous classification

## Data Quality Gates
- Email format validation
- Duplicate detection and removal
- Newsletter/spam filtering
- Contact completeness scoring

## Status
**Active Development** - Application Systems pipeline implementation
**Progress:** CSV processing and classification logic implementation
**Next:** Excel export with professional formatting

## Documentation
- Technical specifications in `docs/`
- Processing logs in `.claude/logs/`
- Data validation rules in `config/`

---

**Project Type:** Application Systems  
**Domain Pipeline:** Agents 0 → 1 → 2 → 3 → 4 → 6 → 7 → 8 → 9 → 12  
**Last Updated:** November 19, 2025