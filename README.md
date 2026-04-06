# Multi-Currency Financial Data Platform on GCP

## Overview

This project simulates an enterprise data engineering solution for a company that operates across multiple countries and manages financial transactions in different currencies.  
The platform ingests official foreign exchange rates from the European Central Bank (ECB) and combines them with financial transactional data to build analytics-ready datasets in Google Cloud Platform (GCP).

The main goal is to centralize financial data, convert amounts into EUR, and generate reliable KPIs for controlling, accounting, and decision-making.

---

## Business Context

This project is inspired by a consulting-style scenario in which a company in the energy sector needs to improve its financial reporting processes.

The organization works with invoices, payments, and vendors across different currencies, which creates challenges such as:
- fragmented financial data,
- manual reporting processes,
- inconsistent currency conversion,
- limited visibility into exchange-rate impact.

The solution is designed as if a data engineering team were contracted to build a cloud-based analytics platform to solve this business problem.

---

## Problem Statement

Many organizations that operate internationally handle financial transactions in multiple currencies. Without a centralized and automated data platform, it becomes difficult to:
- consolidate financial data into a common base currency,
- compare business periods consistently,
- measure exchange-rate exposure,
- and support finance teams with trustworthy reporting.

This project addresses that problem by building a cloud-based multi-currency financial analytics platform on GCP.

---

## Project Objectives

- Ingest official ECB exchange-rate data.
- Integrate financial transactional data.
- Store raw data in Google Cloud Storage and BigQuery.
- Transform and model data into analytics-ready tables.
- Convert invoice amounts into EUR using official FX rates.
- Generate finance-oriented KPIs for reporting and analysis.
- Prepare a presentation layer with Streamlit connected to BigQuery.

---

## Project Scope

### V1 — Cloud Foundation
- Project structure
- GCP setup
- Cloud Storage raw layer
- BigQuery raw dataset
- ECB ingestion pipeline

### V2 — Analytics Layer
- Staging models
- Marts models
- EUR conversion logic
- Financial KPIs

### V3 — Engineering / DevOps
- Repository structure
- Environment configuration
- Data validation
- Logging
- Reproducible execution

### V4 — Presentation Layer
- Streamlit application
- BigQuery connection
- Executive dashboard
- Business insights display

---

## Solution Architecture

```text
ECB API + Financial Transactional Data
                ↓
          Python ingestion
                ↓
     Cloud Storage (raw landing)
                ↓
         BigQuery raw tables
                ↓
       BigQuery staging models
                ↓
         BigQuery marts / KPIs
                ↓
      Streamlit dashboard (V4)

      Technology Stack
Google Cloud Platform (GCP)
Cloud Storage
BigQuery
Python
SQL
Streamlit
Git / GitHub
VS Code
Data Sources
1. European Central Bank (ECB)

Official foreign exchange reference rates used to convert financial amounts into EUR.

2. Financial transactional dataset

A finance-oriented transactional dataset representing invoices, payments, vendors, and business-related financial operations.

3. Complementary modeled entities

Additional supporting dimensions may be created when necessary, such as:

vendors,
cost centers,
currencies,
calendar references.

These are used to simulate a realistic enterprise reporting scenario.

Data Model

The project follows a layered analytical design:

Raw Layer

Stores data as close as possible to the source.

Examples:

raw.ecb_fx_rates
raw.fin_invoices
raw.fin_payments
raw.fin_vendors
Staging Layer

Applies cleaning, standardization, type casting, and basic business rules.

Examples:

staging.stg_fx_rates
staging.stg_invoices
staging.stg_payments
staging.stg_vendors
Marts Layer

Contains analytics-ready data products for business consumption.

Examples:

marts.fact_invoices_eur
marts.fact_payments
marts.dim_vendors
marts.mart_finance_kpis
Key KPIs

The project is designed to generate indicators such as:

Total invoice amount
Total invoice amount converted to EUR
Overdue invoices count
Overdue amount
Average payment delay
Payment compliance rate
Spend by vendor
Spend by month
Currency exposure
FX-adjusted financial trend
Repository Structure
multi-currency-financial-data-platform/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── architecture.md
│   ├── business_case.md
│   └── data_dictionary.md
│
├── sql/
│   ├── raw/
│   ├── staging/
│   └── marts/
│
├── src/
│   ├── extract/
│   ├── load/
│   ├── transform/
│   └── utils/
│
├── streamlit_app/
│
├── tests/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
Prerequisites

Before running the project, make sure you have:

Python 3.10+
A GCP project
BigQuery enabled
Cloud Storage enabled
Google Cloud SDK installed
Proper authentication configured
A service account or local auth setup if required
GCP Configuration

The project is expected to use:

Cloud Storage bucket for raw landing files
BigQuery datasets for:
raw
staging
marts

Suggested naming example:

Bucket: mcfdp-raw-<suffix>
Datasets:
raw
staging
marts
Environment Variables

The project may require environment variables such as:

GCP_PROJECT_ID=your-project-id
GCS_BUCKET_NAME=your-bucket-name
BQ_RAW_DATASET=raw
BQ_STAGING_DATASET=staging
BQ_MARTS_DATASET=marts

Create a .env file locally based on .env.example.

Installation
pip install -r requirements.txt
Execution Flow

A typical execution flow is:

Extract ECB exchange-rate data
Store raw files in Cloud Storage
Load raw data into BigQuery
Run staging transformations
Run marts transformations
Query KPIs
Expose results through Streamlit (V4)
Data Quality Checks

Examples of data quality rules in this project:

exchange-rate date must not be null
invoice amount must be greater than zero
invoice currency must not be null
invoice date must be valid
FX conversion must only happen when a matching rate is available
relationships between invoices and payments must be consistent
Expected Output

The final solution is expected to provide:

a reproducible cloud-based data pipeline,
analytics-ready financial tables in BigQuery,
EUR-normalized financial metrics,
business KPIs for reporting,
and an interactive Streamlit dashboard connected to BigQuery.
Current Limitations
This project does not currently use SAP production data.
Cloud Composer, Dataflow, and streaming are not part of the initial version.
Some supporting entities may be modeled to simulate a realistic business scenario.
Future Improvements
Add workflow orchestration
Add automated testing
Add CI/CD
Add Terraform-based infrastructure setup
Integrate more business dimensions
Extend the Streamlit dashboard with advanced filters and insights
Why This Project Matters

This project is not only a technical exercise. It is designed to simulate a real-world enterprise reporting problem and to demonstrate skills in:

data engineering,
cloud data platforms,
financial data modeling,
analytics,
and professional software/project structure.
Author

Carlos Alberto
Data Engineering / Cybersecurity profile
Project built as a professional portfolio case aligned with enterprise cloud data engineering roles.