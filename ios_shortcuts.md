# 📱 Ingesta de Datos: Atajos de iOS (Shortcuts)

Una de las partes más importantes de cualquier pipeline de datos es la **captura de la información**. Para hacer que el registro de mis finanzas fuera un hábito sostenible, necesitaba que la entrada de datos fuera lo más rápida y con la menor fricción posible.

Para ello, diseñé un **Atajo de iOS** (iOS Shortcut) que funciona como el sistema de ingesta (Source System) de este proyecto.

## ⚙️ ¿Cómo funciona?

El atajo se ejecuta directamente desde la pantalla de inicio de mi iPhone y realiza los siguientes pasos:

1. **Formulario de Entrada (User Input):** 
   Me solicita rellenar rápidamente los campos clave mediante menús desplegables y campos de texto nativos de iOS:
   - Concepto (Ej. "Cena restaurante")
   - Valor (Ej. 25.50)
   - Cuenta (Ej. "Tarjeta de Crédito")
   - Tipo (Gasto/Ingreso)
   - Tipo Detallado (Ej. "Ocio")

2. **Transformación JSON:** 
   El atajo toma mis respuestas, formatea la fecha actual y construye un objeto JSON compatible con la estructura que exige Notion.

3. **Petición HTTP REST (POST API):** 
   Utiliza la acción nativa de iOS "Obtener contenido de URL" (Get contents of URL) para enviar un método `POST` a la API de Notion (`https://api.notion.com/v1/pages`).
   - **Headers:** Incluye mi `Bearer Token` y la versión de Notion.
   - **Body:** Envía el JSON generado en el paso anterior.

## 🚀 Valor para el Pipeline

Gracias a esta solución:
- **Cero latencia en el registro:** Tardo menos de 10 segundos en registrar una transacción en el momento en que ocurre.
- **Datos estructurados desde el origen:** Evito errores tipográficos porque las categorías (Cuentas, Tipos) están predefinidas en los menús del atajo.
- **Automatización Real:** Los datos entran limpios a Notion, lo que facilita el trabajo del script de Python y de Apache Airflow en las fases posteriores del proceso ETL.

---
*Nota: Debido a la naturaleza visual de los Atajos de iOS, no hay "código fuente" directo que subir aquí, pero el mecanismo subyacente es la interacción con APIs RESTful.*