CREATE OR REPLACE TABLE `europ-public-p-fx-d-platform.marts.kpi_supplier_anomalies` AS
SELECT
  supplier_id,
  month_date,
  total_amount_eur,
  lower_bound,
  upper_bound,
  anomaly_probability
FROM `europ-public-p-fx-d-platform.marts.anomaly_supplier_spend`
WHERE is_anomaly = TRUE;