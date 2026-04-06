import streamlit as st
import requests
import pandas as pd

API_BASE_URL = "https://financial-api-484677665897.europe-west1.run.app"

st.set_page_config(page_title="Financial Dashboard", layout="wide")

st.title("Multi-Currency Financial Dashboard")

def get_data(endpoint):
    response = requests.get(f"{API_BASE_URL}{endpoint}")
    return pd.DataFrame(response.json())


# KPIs
kpis = get_data("/kpis/executive-summary")
kpi_map = dict(zip(kpis["kpi_name"], kpis["kpi_value"]))

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Spend EUR", kpi_map.get("total_spend_eur"))
col2.metric("Total Invoices", kpi_map.get("total_invoices"))
col3.metric("FX Exceptions", kpi_map.get("fx_exception_invoices"))
col4.metric("Supplier Anomalies", kpi_map.get("supplier_anomalies"))


# Monthly Spend
st.subheader("Monthly Spend (EUR)")
monthly = get_data("/kpis/monthly-spend")
st.line_chart(monthly.set_index("month_date")["total_amount_eur"])


# Top Suppliers
st.subheader("Top Suppliers")
top_suppliers = get_data("/kpis/top-suppliers")
st.dataframe(top_suppliers)


# Currency Exposure
st.subheader("Currency Exposure")
currency = get_data("/kpis/currency-exposure")
st.dataframe(currency)


# FX Exceptions
st.subheader("FX Exceptions")
fx = get_data("/kpis/fx-exceptions")
st.dataframe(fx)


# Anomalies
st.subheader("Supplier Anomalies")
anomalies = get_data("/kpis/supplier-anomalies")
st.dataframe(anomalies)