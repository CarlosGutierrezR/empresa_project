SELECT 'kpi_executive_summary' AS table_name, COUNT(*) AS row_count
FROM `europ-public-p-fx-d-platform.marts.kpi_executive_summary`

UNION ALL

SELECT 'kpi_monthly_spend_eur' AS table_name, COUNT(*) AS row_count
FROM `europ-public-p-fx-d-platform.marts.kpi_monthly_spend_eur`

UNION ALL

SELECT 'kpi_top_suppliers' AS table_name, COUNT(*) AS row_count
FROM `europ-public-p-fx-d-platform.marts.kpi_top_suppliers`

UNION ALL

SELECT 'kpi_currency_exposure' AS table_name, COUNT(*) AS row_count
FROM `europ-public-p-fx-d-platform.marts.kpi_currency_exposure`

UNION ALL

SELECT 'kpi_fx_exceptions' AS table_name, COUNT(*) AS row_count
FROM `europ-public-p-fx-d-platform.marts.kpi_fx_exceptions`

UNION ALL

SELECT 'kpi_supplier_anomalies_enriched' AS table_name, COUNT(*) AS row_count
FROM `europ-public-p-fx-d-platform.marts.kpi_supplier_anomalies_enriched`;