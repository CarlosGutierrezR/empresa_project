CREATE OR REPLACE TABLE `europ-public-p-fx-d-platform.marts.kpi_executive_summary` AS
WITH total_spend AS (
  SELECT
    'total_spend_eur' AS kpi_name,
    CAST(SUM(amount_eur) AS STRING) AS kpi_value
  FROM `europ-public-p-fx-d-platform.marts.fact_ap_invoices_eur`
),
total_invoices AS (
  SELECT
    'total_invoices' AS kpi_name,
    CAST(COUNT(*) AS STRING) AS kpi_value
  FROM `europ-public-p-fx-d-platform.marts.fact_ap_invoices_eur`
),
fx_exceptions AS (
  SELECT
    'fx_exception_invoices' AS kpi_name,
    CAST(COUNT(*) AS STRING) AS kpi_value
  FROM `europ-public-p-fx-d-platform.marts.fact_ap_invoices_eur`
  WHERE amount_eur IS NULL
),
supplier_anomalies AS (
  SELECT
    'supplier_anomalies' AS kpi_name,
    CAST(COUNT(*) AS STRING) AS kpi_value
  FROM `europ-public-p-fx-d-platform.marts.kpi_supplier_anomalies_enriched`
)
SELECT * FROM total_spend
UNION ALL
SELECT * FROM total_invoices
UNION ALL
SELECT * FROM fx_exceptions
UNION ALL
SELECT * FROM supplier_anomalies;