CREATE OR REPLACE TABLE `europ-public-p-fx-d-platform.marts.kpi_top_suppliers` AS
SELECT
  supplier_id,
  supplier_name,
  invoice_count,
  total_amount_original,
  total_amount_eur
FROM `europ-public-p-fx-d-platform.marts.kpi_supplier_spend`
ORDER BY total_amount_eur DESC
LIMIT 10;