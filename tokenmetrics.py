import streamlit as st
import requests

# URL del endpoint de informes de IA
url = "https://api.tokenmetrics.com/v2/ai-reports"

# Clave de API
api_key = "tu_clave_de_api_aqui"

# Encabezados de la solicitud
headers = {
    "accept": "application/json",
    "api_key": api_key
}

# Realizar la solicitud GET
response = requests.get(url, headers=headers)

# Verificar el estado de la respuesta
if response.status_code == 200:
    # Parsear la respuesta JSON
    data = response.json()
    
    # Mostrar los informes en el dashboard
    st.write("Informes de IA:")
    for report in data["data"]:
        st.write(report)
else:
    st.error("Error al obtener los informes de IA. Código de estado:", response.status_code)
