Descripción del proyecto

Este proyecto consiste en el diseño e implementación de una plataforma de datos en la nube orientada a resolver un problema real del ámbito empresarial: la gestión y análisis de información financiera en múltiples monedas.

La solución permite integrar datos financieros con tipos de cambio oficiales del Banco Central Europeo (ECB), transformarlos y generar indicadores clave en una moneda común (EUR), facilitando la toma de decisiones en áreas como controlling y accounting.

🧠 Contexto de negocio

Simulamos un escenario donde una empresa del sector energético opera en distintos países y trabaja con múltiples monedas.

Esto genera problemas como:

❌ Datos financieros dispersos
❌ Procesos manuales de reporting
❌ Conversión de divisas inconsistente
❌ Baja visibilidad del impacto del tipo de cambio

Para resolverlo, se plantea una solución como si un equipo de ingeniería de datos (nuestro equipo del Bootcamp) fuera contratado para construir una plataforma cloud escalable y analítica.

🎯 Objetivo

Construir una plataforma que sea capaz de:

💱 Consolidar datos financieros multi-moneda en EUR
📊 Analizar el impacto de los tipos de cambio
📈 Generar KPIs financieros consistentes
⚠️ Detectar anomalías en el gasto
🧑‍💼 Proporcionar visualización para negocio
🏗️ Arquitectura de la solución
ECB + Datos financieros (ERP-like)
                ↓
        Ingesta con Python
                ↓
   Cloud Storage (capa raw)
                ↓
        BigQuery (raw)
                ↓
     BigQuery (staging)
                ↓
       BigQuery (marts)
                ↓
 API (FastAPI en Cloud Run)
                ↓
   Dashboard (Streamlit)
🛠️ Tecnologías utilizadas
☁️ Google Cloud Platform (GCP)
🪣 Cloud Storage
📊 BigQuery
🐍 Python
🧾 SQL
⚡ FastAPI
🐳 Docker
🚀 Cloud Run
📈 Streamlit
🔧 Git / GitHub
📂 Fuentes de datos
1. 📊 ECB (European Central Bank)

Tipos de cambio oficiales utilizados para convertir importes a EUR.

2. 🧾 Dataset financiero (simulado)

Incluye información de:

facturas
proveedores
órdenes de compra
requisiciones
🧱 Modelo de datos

El proyecto sigue una arquitectura por capas:

🔹 Raw

Datos originales sin transformar

Ejemplo:

raw.ecb_fx_rates
raw.oracle_invoices
🔹 Staging

Limpieza y estandarización

Tipado correcto
Normalización de moneda
Reglas básicas de negocio
🔹 Marts

Datos listos para análisis

Principales tablas:

fact_ap_invoices_eur → facturas convertidas a EUR
kpi_monthly_spend_eur → gasto mensual
kpi_top_suppliers → top proveedores
kpi_currency_exposure → exposición por moneda
kpi_fx_exceptions → errores de conversión
kpi_supplier_anomalies_enriched → anomalías
📊 KPIs generados
💰 Gasto total en EUR
📆 Gasto mensual
🏢 Top proveedores por gasto
🌍 Exposición por moneda
⚠️ Excepciones FX
🤖 Anomalías en gasto
🌐 API en producción

La API está desplegada en Cloud Run:

👉 https://financial-api-484677665897.europe-west1.run.app

Endpoints principales:

/health
/kpis/executive-summary
/kpis/monthly-spend
/kpis/top-suppliers
/kpis/currency-exposure
/kpis/fx-exceptions
/kpis/supplier-anomalies
📊 Dashboard (Streamlit)

Aplicación conectada a la API para visualización:

KPIs principales
Evolución temporal
Ranking de proveedores
Exposición por moneda
Anomalías detectadas
▶️ Cómo ejecutar el proyecto
1. Clonar repositorio
git clone https://github.com/CarlosGutierrezR/empresa_project.git
cd empresa_project
2. Instalar dependencias
pip install -r requirements.txt
3. Ejecutar API en local
uvicorn main:app --reload
4. Ejecutar Streamlit
streamlit run streamlit_app.py
⚙️ Estructura del proyecto
empresa_project/
│
├── src/                  # scripts de ingesta
├── sql/                  # queries analíticas
├── main.py               # API FastAPI
├── streamlit_app.py      # dashboard
├── Dockerfile
├── requirements.txt
├── README.md
🧪 Validaciones realizadas
✔ Conteo de registros en todas las capas
✔ Validación de conversiones FX
✔ Integridad de joins
✔ KPIs coherentes
✔ API funcional en producción
✔ Dashboard operativo
🚧 Limitaciones
Datos simulados (no SAP real)
Sin orquestación (Airflow/Composer)
Sin CI/CD automatizado
🔮 Mejoras futuras
⚙️ Automatización con Cloud Build
🔄 Orquestación de pipelines
🧪 Testing de datos
🏗️ Infraestructura como código (Terraform)
📊 Dashboard más avanzado
💡 Valor del proyecto

Este proyecto demuestra capacidades reales en:

Ingeniería de datos en la nube
Modelado analítico
Integración de datos financieros
Desarrollo de APIs
Arquitectura moderna de datos
Pensamiento orientado a negocio
👨‍💻 Equipo

Proyecto desarrollado como parte del:

🎓 Digital Tech Bootcamp — Proyecto Final
