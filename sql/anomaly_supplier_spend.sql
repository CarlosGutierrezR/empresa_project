CREATE OR REPLACE TABLE `europ-public-p-fx-d-platform.marts.anomaly_supplier_spend` AS
SELECT *
FROM ML.DETECT_ANOMALIES(
  MODEL `europ-public-p-fx-d-platform.marts.bqml_model_supplier_anomaly`,
  STRUCT(0.95 AS anomaly_prob_threshold)
);