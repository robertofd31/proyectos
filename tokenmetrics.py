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
    
    tokens = [(report["TOKEN_NAME"], report["SYMBOL"]) for report in data["data"]]
    
    # Desplegable para seleccionar el token
    selected_token_index = st.selectbox("Selecciona un token:", options=range(len(tokens)))
    
    # Mostrar el informe correspondiente al token seleccionado
    selected_report = data["data"][selected_token_index]
    st.write("Nombre del Token:", selected_report["TOKEN_NAME"])
    st.write("Símbolo del Token:", selected_report["SYMBOL"])
    st.write("Informe de Trader:")
    st.write(selected_report["TRADER_REPORT"])
    st.write("Informe de Tecnología:")
    st.write(selected_report["TECHNOLOGY_REPORT"])
else:
    st.error("Error al obtener los informes de IA. Código de estado:", response.status_code)

