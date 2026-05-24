import os
import requests
import snowflake.connector
from datetime import datetime
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def get_notion_text(prop):
    """Función de ayuda para extraer texto de Notion sin importar el tipo de columna."""
    if not prop: return ""
    if "title" in prop and prop["title"]: return prop["title"][0]["text"]["content"]
    if "rich_text" in prop and prop["rich_text"]: return prop["rich_text"][0]["text"]["content"]
    if "select" in prop and prop["select"]: return prop["select"]["name"]
    return ""

def fetch_notion_data(notion_token, database_id):
    """Extrae datos financieros desde la API de Notion."""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json().get("results", [])

def load_to_snowflake(data):
    """Transforma los datos y los carga en Snowflake."""
    # Obtenemos las credenciales del entorno
    conn = snowflake.connector.connect(
        user=os.getenv("SF_USER"),
        password=os.getenv("SF_PASSWORD"),
        account=os.getenv("SF_ACCOUNT"),
        warehouse=os.getenv("SF_WAREHOUSE"),
        database=os.getenv("SF_DATABASE"),
        schema=os.getenv("SF_SCHEMA")
    )
    cursor = conn.cursor()
    
    insert_query = """
        INSERT INTO raw_finances 
        (concepto, valor, cuenta, tipo, tipo_detallado, fecha)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    records = []
    for item in data:
        props = item.get("properties", {})
        
        try:
            # Extracción basada en tu estructura de 6 columnas
            concepto = get_notion_text(props.get("Concepto"))
            valor = float(props.get("Valor", {}).get("number", 0.0))
            cuenta = get_notion_text(props.get("Cuenta"))
            tipo = get_notion_text(props.get("Tipo"))
            tipo_detallado = get_notion_text(props.get("Tipo Detallado"))
            
            # Manejo de Fecha: De YYYY-MM-DD (Notion) a DD/MM/YYYY
            fecha_notion = props.get("Fecha", {}).get("date", {}).get("start")
            fecha_formateada = ""
            if fecha_notion:
                fecha_obj = datetime.strptime(fecha_notion, "%Y-%m-%d")
                fecha_formateada = fecha_obj.strftime("%d/%m/%Y")
            
            records.append((concepto, valor, cuenta, tipo, tipo_detallado, fecha_formateada))
            
        except Exception as e:
            print(f"Error parseando registro {item.get('id')}: {e}")
            continue
            
    if records:
        cursor.executemany(insert_query, records)
        conn.commit()
        print(f"Éxito: Se han cargado {len(records)} registros en Snowflake.")
    
    cursor.close()
    conn.close()

def run_etl():
    """Ejecución del pipeline."""
    print("Iniciando extracción desde Notion...")
    
    notion_token = os.getenv("NOTION_TOKEN")
    notion_db_id = os.getenv("NOTION_DATABASE_ID")
    
    if not notion_token or not notion_db_id:
        raise ValueError("Faltan las credenciales de Notion en el archivo .env")
        
    raw_data = fetch_notion_data(notion_token, notion_db_id)
    
    if raw_data:
        print("Datos extraídos. Iniciando carga a Snowflake...")
        load_to_snowflake(raw_data)
    else:
        print("No se encontraron datos en Notion.")

if __name__ == "__main__":
    run_etl()
