CREATE OR REPLACE TABLE `europ-public-p-fx-d-platform.marts.kpi_currency_exposure` AS
SELECT
  currency_code,
  COUNT(*) AS invoice_count,
  SUM(amount_original) AS total_amount_original,
  SUM(amount_eur) AS total_amount_eur,
  COUNTIF(amount_eur IS NULL) AS rows_without_amount_eur
FROM `europ-public-p-fx-d-platform.marts.fact_ap_invoices_eur`
GROUP BY currency_code;