# 🌍 Veritas Fex  
### La verdad de tus números en cualquier moneda

---

## 👥 Equipo de trabajo — Grupo 2

- Juan Castellano Castillero  
- Victoria Torres Torres  
- Carlos Gutiérrez Rondón  
- Alberto Munuera Ramos  

---

## 🧠 Descripción del proyecto

Veritas Fex es una plataforma de datos en la nube diseñada para resolver un problema real del entorno empresarial: la gestión y análisis de información financiera en múltiples monedas.

Muchas organizaciones operan con datos financieros distribuidos en distintos sistemas, con procesos manuales de reporting que dificultan la comparación y el análisis del impacto del tipo de cambio.

Este proyecto simula un escenario de consultoría en el que se diseña e implementa una solución cloud para:

- centralizar datos financieros  
- convertir importes a una moneda base (EUR)  
- generar indicadores analíticos  
- proporcionar una visualización clara para negocio  

---

## 🎯 Problema de negocio

Las empresas que operan en múltiples monedas enfrentan:

- datos fragmentados en distintos sistemas  
- reporting manual y poco escalable  
- dificultad para comparar periodos  
- falta de visibilidad sobre el impacto del tipo de cambio  

Veritas Fex resuelve este problema mediante una plataforma analítica automatizada en GCP.

---

## 🏗️ Arquitectura de la solución

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

---

## 📊 Capas de datos

### 🔹 Raw
Datos originales sin transformar  
- ECB FX rates  
- datos financieros  

### 🔹 Staging
- limpieza  
- normalización  
- tipado  

### 🔹 Marts
- datos listos para negocio  
- KPIs financieros  

---

## 📈 KPIs generados

- Gasto total consolidado en EUR  
- Total de facturas  
- Exposición por moneda  
- Top proveedores  
- Excepciones FX  
- Detección de anomalías  

---

## 🚀 Servicios desplegados

### 🔹 Backend (API)
Cloud Run  
👉 https://financial-api-484677665897.europe-west1.run.app  

Swagger:
👉 /docs  

---

### 🔹 Frontend (Dashboard)
Cloud Run  
👉 https://financial-frontend-484677665897.europe-west1.run.app  

---

## 📦 Contenedores

Imágenes almacenadas en:

👉 Artifact Registry  
Repositorio: `financial-api-repo`

---

## 🔄 Flujo de datos

1. Extracción de datos ECB  
2. Carga en Cloud Storage  
3. Ingesta en BigQuery  
4. Transformación (raw → staging → marts)  
5. Exposición vía API  
6. Consumo en dashboard  

---

## 📅 Planificación del proyecto

- Fase 1: análisis y arquitectura  
- Fase 2: ingesta de datos  
- Fase 3: modelado en BigQuery  
- Fase 4: KPIs  
- Fase 5: dashboard  
- Fase 6: validación y documentación  

---

## 🎯 Resultado final

La solución permite:

- consolidar información financiera en EUR  
- analizar impacto del tipo de cambio  
- generar indicadores fiables  
- proporcionar un dashboard interactivo  

---

## ⚠️ Limitaciones actuales

- No se utilizan datos reales de SAP  
- No hay automatización CI/CD en esta versión  
- No se implementa streaming  

---

## 🔮 Mejoras futuras

- CI/CD con GitHub Actions  
- orquestación con Cloud Composer  
- mayor granularidad en KPIs  
- mejoras en visualización  

---

## 💼 Valor profesional

Este proyecto demuestra capacidades en:

- ingeniería de datos  
- modelado analítico  
- arquitectura cloud  
- desarrollo backend  
- visualización de datos  
- enfoque de negocio  

---
👨‍💻 Equipo

Proyecto desarrollado como parte del:

🎓 Digital Tech Bootcamp — Proyecto Final - Grupo # 2
