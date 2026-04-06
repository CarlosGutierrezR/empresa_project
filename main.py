from fastapi import FastAPI
from google.cloud import bigquery

app = FastAPI(title="Multi-Currency Financial Data API")

client = bigquery.Client(project="europ-public-p-fx-d-platform")


def run_query(query: str):
    rows = client.query(query).result()
    return [dict(row.items()) for row in rows]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/kpis/executive-summary")
def get_executive_summary():
    query = """
    SELECT *
    FROM `europ-public-p-fx-d-platform.marts.kpi_executive_summary`
    ORDER BY kpi_name
    """
    return run_query(query)


@app.get("/kpis/monthly-spend")
def get_monthly_spend():
    query = """
    SELECT *
    FROM `europ-public-p-fx-d-platform.marts.kpi_monthly_spend_eur`
    ORDER BY month_date
    """
    return run_query(query)


@app.get("/kpis/top-suppliers")
def get_top_suppliers():
    query = """
    SELECT *
    FROM `europ-public-p-fx-d-platform.marts.kpi_top_suppliers`
    ORDER BY total_amount_eur DESC
    """
    return run_query(query)


@app.get("/kpis/currency-exposure")
def get_currency_exposure():
    query = """
    SELECT *
    FROM `europ-public-p-fx-d-platform.marts.kpi_currency_exposure`
    ORDER BY currency_code
    """
    return run_query(query)


@app.get("/kpis/fx-exceptions")
def get_fx_exceptions():
    query = """
    SELECT *
    FROM `europ-public-p-fx-d-platform.marts.kpi_fx_exceptions`
    """
    return run_query(query)


@app.get("/kpis/supplier-anomalies")
def get_supplier_anomalies():
    query = """
    SELECT *
    FROM `europ-public-p-fx-d-platform.marts.kpi_supplier_anomalies_enriched`
    ORDER BY anomaly_probability DESC
    """
    return run_query(query)

@app.get("/")
def root():
    return {
        "message": "Multi-Currency Financial Data API is running",
        "docs_url": "/docs",
        "health_url": "/health"
    }