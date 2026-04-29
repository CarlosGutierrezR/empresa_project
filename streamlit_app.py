import os
from html import escape

import altair as alt
import pandas as pd
import requests
import streamlit as st

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://financial-api-484677665897.europe-west1.run.app",
)

st.set_page_config(
    page_title="Panel Ejecutivo Financiero Multi-Moneda",
    layout="wide",
    initial_sidebar_state="expanded",
)

MONTH_NAMES_ES = {
    1: "ene",
    2: "feb",
    3: "mar",
    4: "abr",
    5: "may",
    6: "jun",
    7: "jul",
    8: "ago",
    9: "sep",
    10: "oct",
    11: "nov",
    12: "dic",
}

COLUMN_LABELS = {
    "supplier_id": "ID proveedor",
    "supplier_name": "Proveedor",
    "invoice_id": "ID factura",
    "invoice_count": "Facturas",
    "month_date": "Mes",
    "invoice_date": "Fecha de factura",
    "currency_code": "Moneda",
    "total_amount_original": "Monto original agregado",
    "amount_original": "Monto original",
    "total_amount_eur": "Gasto consolidado (EUR)",
    "amount_eur": "Importe convertido (EUR)",
    "rows_without_amount_eur": "Registros sin conversion a EUR",
    "fx_rate": "Tipo de cambio",
    "exchange_rate": "Tipo de cambio",
    "exchange_rate_date": "Fecha de tipo de cambio",
    "exception_reason": "Motivo de excepcion",
    "lower_bound": "Limite inferior (EUR)",
    "upper_bound": "Limite superior (EUR)",
    "anomaly_probability": "Probabilidad de anomalia",
    "kpi_name": "Indicador",
    "kpi_value": "Valor",
}

KPI_CONFIG = [
    {
        "key": "total_spend_eur",
        "label": "Gasto total consolidado",
        "help": (
            "Resume el gasto total convertido a EUR para disponer de una vista "
            "financiera unica y comparable."
        ),
        "formatter": "currency",
    },
    {
        "key": "total_invoices",
        "label": "Total de facturas",
        "help": (
            "Mide el volumen operativo analizado por la plataforma y ayuda a "
            "dimensionar el alcance del proceso financiero."
        ),
        "formatter": "integer",
    },
    {
        "key": "fx_exception_invoices",
        "label": "Excepciones FX",
        "help": (
            "Identifica facturas sin conversion valida a EUR para controlar el "
            "impacto del tipo de cambio y la calidad del dato."
        ),
        "formatter": "integer",
    },
    {
        "key": "supplier_anomalies",
        "label": "Anomalias relevantes",
        "help": (
            "Senala proveedores con patrones de gasto atipicos para priorizar "
            "revisiones y seguimiento ejecutivo."
        ),
        "formatter": "integer",
    },
]


def inject_styles():
    st.markdown(
        """
        <style>
        html, body, [class*="css"] {
            font-family: "Aptos", "Segoe UI", "Trebuchet MS", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(37, 99, 235, 0.10), transparent 28%),
                radial-gradient(circle at top right, rgba(15, 118, 110, 0.08), transparent 26%),
                linear-gradient(180deg, #f6f8fb 0%, #eef3f8 100%);
            color: #0f172a;
        }

        .block-container {
            max-width: 1280px;
            padding-top: 1.75rem;
            padding-bottom: 3rem;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        .hero-card {
            background: linear-gradient(135deg, #0f172a 0%, #173a74 56%, #0f766e 100%);
            border-radius: 26px;
            padding: 2.2rem 2.35rem;
            color: #f8fafc;
            box-shadow: 0 24px 56px rgba(15, 23, 42, 0.22);
            margin-bottom: 1.35rem;
        }

        .hero-eyebrow {
            margin: 0 0 0.7rem 0;
            font-size: 0.82rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-weight: 700;
            color: #bfdbfe;
        }

        .hero-title {
            margin: 0;
            font-size: 2.3rem;
            line-height: 1.15;
            font-weight: 800;
        }

        .hero-subtitle {
            margin: 0.85rem 0 0 0;
            max-width: 920px;
            font-size: 1rem;
            line-height: 1.72;
            color: rgba(248, 250, 252, 0.93);
        }

        .hero-pill-row {
            margin-top: 1rem;
        }

        .hero-pill {
            display: inline-block;
            margin: 0.25rem 0.45rem 0 0;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            background: rgba(255, 255, 255, 0.12);
            font-size: 0.84rem;
            font-weight: 600;
        }

        .section-tag {
            margin: 0 0 0.2rem 0;
            color: #2563eb;
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .section-title {
            margin: 0;
            font-size: 1.35rem;
            font-weight: 800;
            color: #0f172a;
        }

        .section-copy {
            margin: 0.45rem 0 1rem 0;
            font-size: 0.97rem;
            line-height: 1.65;
            color: #475569;
        }

        .section-separator {
            margin: 1.45rem 0 0.9rem 0;
            border-top: 1px solid rgba(148, 163, 184, 0.36);
        }

        .kpi-card {
            min-height: 172px;
            background: rgba(255, 255, 255, 0.97);
            border: 1px solid #dce4ec;
            border-radius: 22px;
            padding: 1.15rem 1.15rem 1rem 1.15rem;
            box-shadow: 0 16px 36px rgba(15, 23, 42, 0.08);
        }

        .kpi-accent {
            width: 48px;
            height: 4px;
            margin-bottom: 0.9rem;
            border-radius: 999px;
            background: linear-gradient(90deg, #2563eb 0%, #0f766e 100%);
        }

        .kpi-label {
            margin: 0;
            color: #334155;
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .kpi-value {
            margin: 0.8rem 0 0.45rem 0;
            color: #0f172a;
            font-size: 1.92rem;
            line-height: 1.08;
            font-weight: 800;
        }

        .kpi-help {
            margin: 0;
            color: #64748b;
            font-size: 0.92rem;
            line-height: 1.55;
        }

        .viz-title {
            margin: 0.1rem 0 0.22rem 0;
            color: #0f172a;
            font-size: 1rem;
            font-weight: 700;
        }

        .viz-copy {
            margin: 0 0 0.8rem 0;
            color: #64748b;
            font-size: 0.9rem;
            line-height: 1.58;
        }

        div[data-testid="stDataFrame"] {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid #dce4ec;
            border-radius: 20px;
            padding: 0.4rem;
            box-shadow: 0 14px 32px rgba(15, 23, 42, 0.06);
            overflow: hidden;
        }

        div[data-testid="stVegaLiteChart"] {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid #dce4ec;
            border-radius: 20px;
            padding: 0.5rem;
            box-shadow: 0 14px 32px rgba(15, 23, 42, 0.06);
            overflow: hidden;
        }

        .stAlert {
            border-radius: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(ttl=300, show_spinner=False)
def get_data(endpoint):
    url = f"{API_BASE_URL}{endpoint}"

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        payload = response.json()
    except requests.exceptions.RequestException as exc:
        st.error(f"No se pudo consultar la API en {endpoint}: {exc}")
        return pd.DataFrame()
    except ValueError:
        st.error(f"La API devolvio una respuesta no valida en {endpoint}.")
        return pd.DataFrame()

    if isinstance(payload, list):
        return pd.DataFrame(payload)

    if isinstance(payload, dict):
        return pd.DataFrame([payload])

    return pd.DataFrame()


def coerce_number(value):
    if value is None or (isinstance(value, str) and not value.strip()):
        return None

    try:
        return float(str(value).strip().replace(",", ""))
    except (TypeError, ValueError):
        return None


def format_number_es(value, decimals=0):
    formatted = f"{value:,.{decimals}f}"
    return formatted.replace(",", "_").replace(".", ",").replace("_", ".")


def format_integer(value):
    number = coerce_number(value)
    if number is None:
        return "Sin dato" if pd.isna(value) else str(value)
    return format_number_es(round(number), 0)


def format_decimal(value):
    number = coerce_number(value)
    if number is None:
        return "Sin dato" if pd.isna(value) else str(value)
    return format_number_es(number, 2)


def format_currency_eur(value):
    number = coerce_number(value)
    if number is None:
        return "Sin dato" if pd.isna(value) else str(value)
    return f"{format_number_es(number, 2)} EUR"


def format_percent(value):
    number = coerce_number(value)
    if number is None:
        return "Sin dato" if pd.isna(value) else str(value)
    percent_value = number * 100 if abs(number) <= 1 else number
    return f"{format_number_es(percent_value, 2)} %"


def format_identifier(value):
    text_value = str(value)
    return text_value[:-2] if text_value.endswith(".0") else text_value


def format_month_year_es(value):
    date_value = pd.to_datetime(value, errors="coerce")
    if pd.isna(date_value):
        return "Sin dato" if pd.isna(value) else str(value)
    return f"{MONTH_NAMES_ES[date_value.month]} {date_value.year}"


def format_date_es(value):
    date_value = pd.to_datetime(value, errors="coerce")
    if pd.isna(date_value):
        return "Sin dato" if pd.isna(value) else str(value)
    return date_value.strftime("%d/%m/%Y")


def humanize_column_name(column_name):
    if column_name in COLUMN_LABELS:
        return COLUMN_LABELS[column_name]
    return column_name.replace("_", " ").strip().capitalize()


def format_value(column_name, value):
    if pd.isna(value):
        return "Sin dato"

    normalized_name = column_name.lower()

    if normalized_name.endswith("_id") or normalized_name == "id":
        return format_identifier(value)

    if normalized_name == "month_date":
        return format_month_year_es(value)

    if normalized_name.endswith("_date") or normalized_name == "date":
        return format_date_es(value)

    if any(token in normalized_name for token in ["probability", "percent", "pct", "ratio"]):
        return format_percent(value)

    if any(
        token in normalized_name
        for token in ["amount_eur", "total_amount_eur", "lower_bound", "upper_bound", "spend_eur"]
    ):
        return format_currency_eur(value)

    if "amount_original" in normalized_name:
        return format_decimal(value)

    if any(token in normalized_name for token in ["count", "rows_without_amount_eur", "invoices"]):
        return format_integer(value)

    number = coerce_number(value)
    if number is None:
        return str(value)

    return format_decimal(number) if not float(number).is_integer() else format_integer(number)


def format_kpi_value(formatter, value):
    if formatter == "currency":
        return format_currency_eur(value)
    if formatter == "integer":
        return format_integer(value)
    if formatter == "percent":
        return format_percent(value)
    return str(value)


def prepare_display_dataframe(df, column_order=None):
    if df.empty:
        return df

    ordered_columns = [column for column in (column_order or list(df.columns)) if column in df.columns]
    ordered_columns.extend([column for column in df.columns if column not in ordered_columns])

    display_df = pd.DataFrame()
    for column in ordered_columns:
        display_df[humanize_column_name(column)] = df[column].apply(
            lambda item, current_column=column: format_value(current_column, item)
        )

    return display_df


def dataframe_height(df, max_rows=10):
    visible_rows = max(1, min(len(df), max_rows))
    return 76 + (visible_rows * 35)


def render_hero():
    st.markdown(
        """
        <div class="hero-card">
            <p class="hero-eyebrow">Veritas Fex — Plataforma Financiera Multi-Moneda en GCP</p>
            <h1 class="hero-title">Panel ejecutivo para consolidacion financiera, analisis FX e indicadores de negocio</h1>
            <p class="hero-subtitle">
                Este dashboard convierte informacion financiera multi-moneda a EUR en una lectura clara para negocio.
                La vista integra gasto total consolidado, evolucion mensual, proveedores de mayor impacto, exposicion por
                moneda, excepciones de conversion FX y anomalias relevantes, consumiendo la API desplegada en Cloud Run.
            </p>
            <div class="hero-pill-row">
                <span class="hero-pill">Consolidacion multi-moneda en EUR</span>
                <span class="hero-pill">Impacto del tipo de cambio</span>
                <span class="hero-pill">KPIs ejecutivos para negocio</span>
                <span class="hero-pill">Filtros interactivos</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(tag, title, description):
    st.markdown(
        f"""
        <p class="section-tag">{escape(tag)}</p>
        <h2 class="section-title">{escape(title)}</h2>
        <p class="section-copy">{escape(description)}</p>
        """,
        unsafe_allow_html=True,
    )


def render_viz_header(title, description):
    st.markdown(
        f"""
        <p class="viz-title">{escape(title)}</p>
        <p class="viz-copy">{escape(description)}</p>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_cards(kpi_map):
    columns = st.columns(len(KPI_CONFIG))

    for column, kpi in zip(columns, KPI_CONFIG):
        with column:
            formatted_value = format_kpi_value(kpi["formatter"], kpi_map.get(kpi["key"]))
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-accent"></div>
                    <p class="kpi-label">{escape(kpi["label"])}</p>
                    <p class="kpi-value">{escape(formatted_value)}</p>
                    <p class="kpi-help">{escape(kpi["help"])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def build_monthly_chart(df):
    if "month_date" not in df.columns or "total_amount_eur" not in df.columns:
        return None

    chart_df = df.copy()
    chart_df["month_date"] = pd.to_datetime(chart_df["month_date"], errors="coerce")
    chart_df["total_amount_eur"] = pd.to_numeric(chart_df["total_amount_eur"], errors="coerce")

    if "invoice_count" in chart_df.columns:
        chart_df["invoice_count"] = pd.to_numeric(chart_df["invoice_count"], errors="coerce")

    chart_df = chart_df.dropna(subset=["month_date", "total_amount_eur"]).sort_values("month_date")
    if chart_df.empty:
        return None

    chart_df["mes"] = chart_df["month_date"].apply(format_month_year_es)
    chart_df["gasto_tooltip"] = chart_df["total_amount_eur"].apply(format_currency_eur)

    tooltip_fields = [
        alt.Tooltip("mes:N", title="Mes"),
        alt.Tooltip("gasto_tooltip:N", title="Gasto consolidado"),
    ]

    if "invoice_count" in chart_df.columns:
        chart_df["facturas_tooltip"] = chart_df["invoice_count"].apply(format_integer)
        tooltip_fields.append(alt.Tooltip("facturas_tooltip:N", title="Facturas"))

    base = alt.Chart(chart_df).encode(
        x=alt.X(
            "mes:N",
            sort=chart_df["mes"].tolist(),
            title="Mes",
            axis=alt.Axis(labelAngle=0, labelPadding=10),
        ),
        y=alt.Y("total_amount_eur:Q", title="Gasto consolidado (EUR)"),
        tooltip=tooltip_fields,
    )

    area = base.mark_area(color="#93c5fd", opacity=0.22)
    line = base.mark_line(color="#0f766e", strokeWidth=3)
    points = base.mark_circle(color="#0f172a", size=58)

    return (
        area + line + points
    ).properties(height=360).configure_view(strokeWidth=0).configure_axis(
        gridColor="#e2e8f0",
        labelColor="#475569",
        titleColor="#0f172a",
        domainColor="#cbd5e1",
    )


def build_horizontal_bar_chart(df, category_column, value_column, axis_title, color):
    if category_column not in df.columns or value_column not in df.columns:
        return None

    chart_df = df.copy()
    chart_df[value_column] = pd.to_numeric(chart_df[value_column], errors="coerce")
    chart_df = chart_df.dropna(subset=[category_column, value_column]).sort_values(value_column, ascending=False)

    if chart_df.empty:
        return None

    chart_df[category_column] = chart_df[category_column].astype(str)
    chart_df["valor_tooltip"] = chart_df[value_column].apply(format_currency_eur)

    tooltip_fields = [
        alt.Tooltip(f"{category_column}:N", title=humanize_column_name(category_column)),
        alt.Tooltip("valor_tooltip:N", title=humanize_column_name(value_column)),
    ]

    if "invoice_count" in chart_df.columns:
        chart_df["facturas_tooltip"] = chart_df["invoice_count"].apply(format_integer)
        tooltip_fields.append(alt.Tooltip("facturas_tooltip:N", title="Facturas"))

    return (
        alt.Chart(chart_df)
        .mark_bar(color=color, cornerRadiusTopRight=7, cornerRadiusBottomRight=7)
        .encode(
            y=alt.Y(f"{category_column}:N", sort="-x", title=None),
            x=alt.X(f"{value_column}:Q", title=axis_title),
            tooltip=tooltip_fields,
        )
        .properties(height=max(260, min(520, len(chart_df) * 42)))
        .configure_view(strokeWidth=0)
        .configure_axis(
            gridColor="#e2e8f0",
            labelColor="#475569",
            titleColor="#0f172a",
            domainColor="#cbd5e1",
        )
    )


def render_dataframe(df, column_order=None, max_rows=10):
    if df.empty:
        st.info("No hay registros disponibles para esta visual con los filtros actuales.")
        return

    display_df = prepare_display_dataframe(df, column_order=column_order)
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=dataframe_height(display_df, max_rows=max_rows),
    )


def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8-sig")


def render_download_button(df, label, filename, key):
    if df.empty:
        return

    st.download_button(
        label=label,
        data=to_csv_bytes(df),
        file_name=filename,
        mime="text/csv",
        key=key,
        use_container_width=True,
    )


def normalize_month_column(df):
    if df.empty or "month_date" not in df.columns:
        return df

    result = df.copy()
    result["month_date"] = pd.to_datetime(result["month_date"], errors="coerce")
    return result


def filter_by_month_range(df, selected_range):
    if df.empty or "month_date" not in df.columns or not selected_range:
        return df

    result = normalize_month_column(df)
    if result["month_date"].isna().all():
        return result

    start_month, end_month = selected_range
    start_month = pd.to_datetime(start_month)
    end_month = pd.to_datetime(end_month)

    return result[
        (result["month_date"] >= start_month)
        & (result["month_date"] <= end_month)
    ]


def filter_by_values(df, column_name, selected_values):
    if df.empty or column_name not in df.columns or not selected_values:
        return df

    return df[df[column_name].astype(str).isin(selected_values)]


def get_available_values(df, column_name):
    if df.empty or column_name not in df.columns:
        return []

    return sorted(df[column_name].dropna().astype(str).unique().tolist())


def get_month_options(*dataframes):
    month_values = []

    for df in dataframes:
        if df.empty or "month_date" not in df.columns:
            continue

        months = pd.to_datetime(df["month_date"], errors="coerce").dropna()
        month_values.extend(months.tolist())

    if not month_values:
        return []

    unique_months = sorted(pd.Series(month_values).drop_duplicates().tolist())
    return unique_months


def render_sidebar_filters(monthly, top_suppliers, currency, fx, anomalies):
    st.sidebar.title("Filtros de negocio")
    st.sidebar.caption(
        "Los filtros modifican las visualizaciones disponibles en la app. "
        "Los KPIs ejecutivos superiores son globales porque la API actual devuelve agregados ya calculados."
    )

    selected_view = st.sidebar.radio(
        "Vista de analisis",
        [
            "Dashboard completo",
            "Resumen ejecutivo",
            "Tendencia mensual",
            "Proveedores",
            "Exposicion FX",
            "Excepciones FX",
            "Anomalias",
        ],
        index=0,
    )

    month_options = get_month_options(monthly, anomalies)
    if month_options:
        selected_month_range = st.sidebar.select_slider(
            "Periodo",
            options=month_options,
            value=(month_options[0], month_options[-1]),
            format_func=format_month_year_es,
        )
    else:
        selected_month_range = None

    currency_options = get_available_values(currency, "currency_code")
    if not currency_options:
        currency_options = get_available_values(fx, "currency_code")

    selected_currencies = st.sidebar.multiselect(
        "Monedas",
        options=currency_options,
        default=currency_options,
    )

    supplier_options = get_available_values(top_suppliers, "supplier_name")
    anomaly_supplier_options = get_available_values(anomalies, "supplier_name")
    supplier_options = sorted(set(supplier_options + anomaly_supplier_options))

    selected_suppliers = st.sidebar.multiselect(
        "Proveedores",
        options=supplier_options,
        default=supplier_options,
    )

    max_rows = st.sidebar.slider(
        "Filas visibles por tabla",
        min_value=5,
        max_value=25,
        value=10,
        step=5,
    )

    st.sidebar.divider()
    st.sidebar.caption(f"API activa: {API_BASE_URL}")

    return {
        "selected_view": selected_view,
        "selected_month_range": selected_month_range,
        "selected_currencies": selected_currencies,
        "selected_suppliers": selected_suppliers,
        "max_rows": max_rows,
    }


def render_executive_summary(kpi_map):
    render_section_header(
        "Resumen ejecutivo",
        "Indicadores clave para negocio",
        (
            "Estos KPIs sintetizan el estado financiero consolidado en EUR, el volumen operativo y los focos "
            "de riesgo que requieren seguimiento ejecutivo."
        ),
    )
    render_kpi_cards(kpi_map)


def render_monthly_section(monthly, max_rows):
    render_section_header(
        "Tendencia de gasto",
        "Evolucion mensual del gasto consolidado",
        (
            "Esta vista ayuda a mostrar el gasto mensual consolidado en EUR y a detectar cambios de tendencia "
            "sin depender de la moneda original de cada factura."
        ),
    )
    render_viz_header(
        "Gasto mensual consolidado en EUR",
        (
            "Ayuda a entender la evolucion del gasto total consolidado y a medir el objetivo del proyecto de "
            "unificar la lectura financiera multi-moneda en una base comparable."
        ),
    )

    monthly_chart = build_monthly_chart(monthly)
    if monthly_chart is not None:
        st.altair_chart(monthly_chart, use_container_width=True)
    else:
        st.info("No se pudo construir el grafico mensual con los datos disponibles.")

    with st.expander("Ver detalle mensual"):
        render_dataframe(
            monthly,
            column_order=["month_date", "invoice_count", "total_amount_eur"],
            max_rows=max_rows,
        )
        render_download_button(
            monthly,
            "Descargar detalle mensual CSV",
            "veritas_fex_gasto_mensual.csv",
            "download_monthly",
        )


def render_suppliers_section(top_suppliers, max_rows):
    render_section_header(
        "Concentracion de gasto",
        "Top proveedores por gasto",
        (
            "Esta seccion ayuda a identificar los proveedores con mayor impacto economico, priorizar negociacion "
            "y entender donde se concentra el gasto total consolidado."
        ),
    )
    render_viz_header(
        "Ranking visual de proveedores por gasto consolidado",
        (
            "Ayuda a mostrar el objetivo de identificar los proveedores que mas explican el gasto total "
            "consolidado en EUR."
        ),
    )

    top_suppliers_chart = build_horizontal_bar_chart(
        top_suppliers,
        category_column="supplier_name",
        value_column="total_amount_eur",
        axis_title="Gasto consolidado (EUR)",
        color="#2563eb",
    )

    if top_suppliers_chart is not None:
        st.altair_chart(top_suppliers_chart, use_container_width=True)
    else:
        st.info("No se pudo construir el grafico de proveedores con los datos disponibles.")

    render_viz_header(
        "Detalle de proveedores con mayor gasto",
        (
            "Ayuda a profundizar en el volumen de facturas y el gasto consolidado para apoyar decisiones "
            "de seguimiento comercial y control financiero."
        ),
    )
    render_dataframe(
        top_suppliers,
        column_order=[
            "supplier_name",
            "supplier_id",
            "invoice_count",
            "total_amount_eur",
            "total_amount_original",
        ],
        max_rows=max_rows,
    )
    render_download_button(
        top_suppliers,
        "Descargar proveedores CSV",
        "veritas_fex_top_proveedores.csv",
        "download_suppliers",
    )


def render_currency_section(currency, max_rows):
    render_section_header(
        "Exposicion por divisa",
        "Impacto de las monedas sobre el gasto",
        (
            "Esta seccion ayuda a analizar el impacto del tipo de cambio, entender la exposicion por moneda "
            "y visualizar cuantas filas no lograron consolidarse correctamente a EUR."
        ),
    )
    render_viz_header(
        "Exposicion consolidada por moneda",
        (
            "Ayuda a explicar el objetivo del proyecto de medir la exposicion por divisa y evaluar donde el "
            "riesgo FX puede ser mas relevante."
        ),
    )

    currency_chart = build_horizontal_bar_chart(
        currency,
        category_column="currency_code",
        value_column="total_amount_eur",
        axis_title="Exposicion consolidada (EUR)",
        color="#0f766e",
    )

    if currency_chart is not None:
        st.altair_chart(currency_chart, use_container_width=True)
    else:
        st.info("No se pudo construir el grafico de exposicion por moneda con los datos disponibles.")

    render_viz_header(
        "Detalle tabular de exposicion por moneda",
        (
            "Ayuda a comparar volumen de facturas, importes originales y conversion a EUR para una lectura "
            "clara del impacto financiero por divisa."
        ),
    )
    render_dataframe(
        currency,
        column_order=[
            "currency_code",
            "invoice_count",
            "total_amount_original",
            "total_amount_eur",
            "rows_without_amount_eur",
        ],
        max_rows=max_rows,
    )
    render_download_button(
        currency,
        "Descargar exposicion por moneda CSV",
        "veritas_fex_exposicion_moneda.csv",
        "download_currency",
    )


def render_fx_exceptions_section(fx, max_rows):
    render_section_header(
        "Control de conversion FX",
        "Excepciones de conversion a EUR",
        (
            "Esta seccion ayuda a detectar registros que no pudieron convertirse correctamente a EUR y, por tanto, "
            "requieren revision para proteger la calidad del dato y el analisis financiero."
        ),
    )
    render_viz_header(
        "Facturas con excepciones de conversion FX",
        (
            "Ayuda a resolver el objetivo de mostrar excepciones de conversion FX para actuar sobre incidencias "
            "que afectan la consolidacion financiera multi-moneda."
        ),
    )
    render_dataframe(fx, max_rows=max_rows)
    render_download_button(
        fx,
        "Descargar excepciones FX CSV",
        "veritas_fex_excepciones_fx.csv",
        "download_fx",
    )


def render_anomalies_section(anomalies, max_rows):
    render_section_header(
        "Deteccion de anomalias",
        "Comportamientos relevantes de proveedores",
        (
            "Esta seccion ayuda a detectar desviaciones de gasto frente a rangos esperados y a priorizar revisiones "
            "de negocio sobre casos potencialmente anormales."
        ),
    )
    render_viz_header(
        "Anomalias relevantes en gasto por proveedor",
        (
            "Ayuda a resolver el objetivo de identificar anomalias relevantes y convertir senales analiticas en "
            "una vista ejecutiva facil de entender."
        ),
    )
    render_dataframe(
        anomalies,
        column_order=[
            "supplier_name",
            "supplier_id",
            "month_date",
            "total_amount_eur",
            "lower_bound",
            "upper_bound",
            "anomaly_probability",
        ],
        max_rows=max_rows,
    )
    render_download_button(
        anomalies,
        "Descargar anomalias CSV",
        "veritas_fex_anomalias.csv",
        "download_anomalies",
    )


def main():
    inject_styles()
    render_hero()

    with st.spinner("Cargando datos desde la API desplegada en Cloud Run..."):
        kpis = get_data("/kpis/executive-summary")
        monthly = get_data("/kpis/monthly-spend")
        top_suppliers = get_data("/kpis/top-suppliers")
        currency = get_data("/kpis/currency-exposure")
        fx = get_data("/kpis/fx-exceptions")
        anomalies = get_data("/kpis/supplier-anomalies")

    if kpis.empty:
        st.error("No se pudieron cargar los KPIs ejecutivos desde la API.")
        st.stop()

    kpi_map = dict(zip(kpis["kpi_name"], kpis["kpi_value"]))

    filters = render_sidebar_filters(monthly, top_suppliers, currency, fx, anomalies)

    monthly_filtered = filter_by_month_range(monthly, filters["selected_month_range"])
    anomalies_filtered = filter_by_month_range(anomalies, filters["selected_month_range"])

    top_suppliers_filtered = filter_by_values(
        top_suppliers,
        "supplier_name",
        filters["selected_suppliers"],
    )
    anomalies_filtered = filter_by_values(
        anomalies_filtered,
        "supplier_name",
        filters["selected_suppliers"],
    )

    currency_filtered = filter_by_values(
        currency,
        "currency_code",
        filters["selected_currencies"],
    )
    fx_filtered = filter_by_values(
        fx,
        "currency_code",
        filters["selected_currencies"],
    )

    selected_view = filters["selected_view"]
    max_rows = filters["max_rows"]

    if selected_view in ["Dashboard completo", "Resumen ejecutivo"]:
        render_executive_summary(kpi_map)
        st.info(
            "Los KPIs ejecutivos son globales. Para recalcularlos por filtros seria necesario "
            "extender la API con parametros de moneda, proveedor y periodo."
        )

    if selected_view == "Dashboard completo":
        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

    if selected_view in ["Dashboard completo", "Tendencia mensual"]:
        render_monthly_section(monthly_filtered, max_rows)

    if selected_view == "Dashboard completo":
        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)
        left_column, right_column = st.columns([1.15, 1])

        with left_column:
            render_suppliers_section(top_suppliers_filtered, max_rows)

        with right_column:
            render_currency_section(currency_filtered, max_rows)

    if selected_view == "Proveedores":
        render_suppliers_section(top_suppliers_filtered, max_rows)

    if selected_view == "Exposicion FX":
        render_currency_section(currency_filtered, max_rows)

    if selected_view == "Dashboard completo":
        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

    if selected_view in ["Dashboard completo", "Excepciones FX"]:
        render_fx_exceptions_section(fx_filtered, max_rows)

    if selected_view == "Dashboard completo":
        st.markdown('<div class="section-separator"></div>', unsafe_allow_html=True)

    if selected_view in ["Dashboard completo", "Anomalias"]:
        render_anomalies_section(anomalies_filtered, max_rows)

    st.caption(
        "Nota: las cifras en EUR representan la consolidacion financiera multi-moneda. "
        "La app consume endpoints FastAPI desplegados en Cloud Run y aplica filtros de visualizacion "
        "sobre los datasets agregados disponibles."
    )


if __name__ == "__main__":
    main()