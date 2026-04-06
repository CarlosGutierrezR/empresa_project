CREATE OR REPLACE TABLE `europ-public-p-fx-d-platform.marts.kpi_monthly_spend_eur` AS
SELECT
  DATE_TRUNC(invoice_date, MONTH) AS month_date,
  COUNT(*) AS invoice_count,
  SUM(amount_original) AS total_amount_original,
  SUM(amount_eur) AS total_amount_eur
FROM `europ-public-p-fx-d-platform.marts.fact_ap_invoices_eur`
GROUP BY month_date
ORDER BY month_date;