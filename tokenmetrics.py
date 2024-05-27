import streamlit as st
import pandas as pd
import requests

def get_price_prediction(symbol):
    url = f"https://api.tokenmetrics.com/v2/price-prediction?symbol={symbol}"
    headers = {"accept": "application/json", "api_key": "tu_clave_de_api_aqui"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["data"][0]["FORECASTS_FOR_NEXT_7_DAYS"]
    else:
        st.error("Error al obtener datos de predicción de precios. Por favor, inténtalo de nuevo más tarde.")
        return None
        
# Define una función para cada página
def home():
    st.title("Welcome to Crypto Reports App")
    st.write("This is the homepage of our Crypto Reports App.")
    st.write("Please select a page from the sidebar.")

def token_reports():
    st.title("Token Reports")
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
    
        # Search box to filter tokens by name
        search_term = st.text_input("Search token by name:")
        
        # Filter tokens by search term
        filtered_tokens = [token for token in tokens if search_term.lower() in token[0].lower()]
        
        # Dropdown to select the token
        selected_token_index = st.selectbox("Select a token:", options=[token[0] for token in filtered_tokens] if filtered_tokens else [token[0] for token in tokens])
        
        if filtered_tokens:
            # Find the index of the selected token
            selected_index = [token[0] for token in filtered_tokens].index(selected_token_index)
        else:
            selected_index = [token[0] for token in tokens].index(selected_token_index)
        
        # Show the report for the selected token
        selected_report = data["data"][selected_index]
        st.write("Token Name:", selected_report["TOKEN_NAME"])
        st.write("Token Symbol:", selected_report["SYMBOL"])
        st.write(selected_report["TRADER_REPORT"])
        st.write("Technology Report:")
        st.write(selected_report["TECHNOLOGY_REPORT"])
    else:
        st.error("Error al obtener los informes de IA. Código de estado:", response.status_code)



def market_metrics():
    st.title("Price Prediction")
    symbol = st.text_input("Enter the symbol of the cryptocurrency (e.g., BTC):")
    if st.button("Get Prediction"):
        if symbol:
            prediction_data = get_price_prediction(symbol)
            if prediction_data:
                df = pd.DataFrame.from_dict(prediction_data, orient="index", columns=["Price Prediction"])
                st.line_chart(df.rename_axis("Date").reset_index())
        else:
            st.warning("Please enter a valid symbol.")


# Definir un diccionario que mapea nombres de página a funciones de página
pages = {
    "Home": home,
    "Token Reports": token_reports,
    "Market Metrics": market_metrics
}

# Barra lateral para la navegación entre páginas
page = st.sidebar.selectbox("Select a page", tuple(pages.keys()))

# Ejecuta la función de la página seleccionada
pages[page]()
