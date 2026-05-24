# 📊 Data Pipeline: Finanzas Personales con Notion, Snowflake y Airflow

Este proyecto es un pipeline de datos *End-to-End* diseñado para extraer, transformar y cargar (ETL) registros de finanzas personales, culminando en un dashboard analítico.

## 🏗️ Arquitectura de Datos

1. **Ingesta Manual:** Uso de Atajos (Shortcuts) de iOS para registrar transacciones de forma ágil en Notion.
2. **Extracción (API REST):** Script en Python que consulta la API de Notion.
3. **Data Warehouse (Snowflake):** Almacenamiento optimizado de los datos extraídos.
4. **Orquestación (Airflow):** Tareas programadas diariamente para mantener los datos actualizados.
5. **Business Intelligence (Power BI):** Dashboard conectado a Snowflake para visualización.

## 🗂️ Modelo de Datos (Notion)

El pipeline está diseñado para procesar una base de datos en Notion con la siguiente estructura:
- **Concepto** (Texto)
- **Valor** (Número decimal)
- **Cuenta** (Texto)
- **Tipo** (Texto - Ingreso/Gasto)
- **Tipo Detallado** (Texto - Categorías)
- **Fecha** (Formateada dinámicamente a `DD/MM/YYYY`)

## ⚙️ Configuración y Despliegue

Para replicar este proyecto sin exponer credenciales, este repositorio utiliza variables de entorno.

1. Clona el repositorio.
2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
3. Renombra el archivo `.env.example` a `.env` y sustituye los valores con tus propias credenciales (Notion Token, Snowflake credentials). **Nota:** El archivo `.env` está ignorado en git por seguridad.
4. Ejecuta el pipeline localmente o despliega la carpeta `/dags` y `/scripts` en tu entorno de Apache Airflow.

## 🚀 Estructura de Ejecución
- **`scripts/extract_load.py`**: Contiene la lógica central de extracción (Notion API) y carga (Snowflake).
- **`dags/notion_to_snowflake_dag.py`**: Es el archivo DAG de Airflow que orquesta e invoca la ejecución del script diariamente.
