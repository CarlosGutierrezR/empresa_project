CREATE OR REPLACE TABLE `europ-public-p-fx-d-platform.marts.kpi_supplier_anomalies_enriched` AS
SELECT
  a.supplier_id,
  s.supplier_name,
  a.month_date,
  a.total_amount_eur,
  a.lower_bound,
  a.upper_bound,
  a.anomaly_probability
FROM `europ-public-p-fx-d-platform.marts.kpi_supplier_anomalies` AS a
LEFT JOIN `europ-public-p-fx-d-platform.marts.dim_suppliers` AS s
  ON a.supplier_id = s.supplier_id;