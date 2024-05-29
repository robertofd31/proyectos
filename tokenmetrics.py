import streamlit as st
import pandas as pd
import requests

@st.cache
def create_correlation_table(correlation_data):
    tokens = [item['token'] for item in correlation_data]
    correlations = [item['correlation'] for item in correlation_data]
    df = pd.DataFrame({'Token': tokens, 'Correlation': correlations})
    return df
    
# Definir el código HTML y CSS para el logotipo y el texto
html_logo = """
<div style="display: flex; align-items: center;">
    <img src="https://assets-global.website-files.com/634054bf0f60201ce9b30604/6513c9b76a4808cda644b737_TM%20Logo_DM.svg" alt="TokenMetrics Logo" style="width: 100px; height: auto; margin-right: 20px;">
    <h1 style="color: #ffcf30;">TokenMetrics.com</h1>
</div>
"""
css_text = """
h1 {
    color: #000000;
    font-size: 36px;
    font-weight: bold;
    margin: 0;
}
"""

# Aplicar el HTML y CSS en Streamlit
st.markdown(html_logo, unsafe_allow_html=True)
st.markdown(f'<style>{css_text}</style>', unsafe_allow_html=True)

def get_bull_and_bear_chart():
    url = "https://api.tokenmetrics.com/v2/market-bull-and-bear-charts"
    headers = {"accept": "application/json", "api_key": "tu_clave_de_api_aqui"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            return data["chartUrl"]
    return None

# Función para obtener el gráfico de Market Cap
def get_market_cap_chart():
    url = "https://api.tokenmetrics.com/v2/total-market-crypto-cap-charts?timeFrame=MAX&chartFilters=total_market_cap%2Caltcoin_market_cap%2Cbtc_market_cap"
    headers = {"accept": "application/json", "api_key": "tu_clave_de_api_aqui"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            return data["chartUrl"]
    return None


def get_price_prediction(symbol):
    url = f"https://api.tokenmetrics.com/v2/price-prediction?symbol={symbol}"
    headers = {"accept": "application/json", "api_key": "tu_clave_de_api_aqui"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Obtener las predicciones de los próximos 7 días
        prediction_data = data["data"][0]["FORECASTS_FOR_NEXT_7_DAYS"]
        # Crear un DataFrame a partir de las predicciones
        df = pd.DataFrame(list(prediction_data.items()), columns=["Day", "Price Prediction"])
        return df
    else:
        st.error("Error al obtener datos de predicción de precios. Por favor, inténtalo de nuevo más tarde.")
        return None
        
# Define una función para cada página
def home():
    st.title("Welcome to the Unofficial TokenMetrics Tool")
    st.write("This tool provides insights and analysis for cryptocurrency trading and investment based on TokenMetrics data.")
    
    # Obtener y mostrar el gráfico de Market Cap
    market_cap_chart_url = get_market_cap_chart()
    if market_cap_chart_url:
        st.image(market_cap_chart_url, caption="Total Market Crypto Cap Chart")
    else:
        st.error("Failed to load Total Market Crypto Cap Chart.")

    # Obtener y mostrar el gráfico Bull and Bear
    bull_and_bear_chart_url = get_bull_and_bear_chart()
    if bull_and_bear_chart_url:
        st.image(bull_and_bear_chart_url, caption="Market Bull and Bear Chart")
    else:
        st.error("Failed to load Market Bull and Bear Chart.")


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
            prediction_df = get_price_prediction(symbol)
            if prediction_df is not None:
                st.line_chart(prediction_df.set_index("Day"), use_container_width=True)
        else:
            st.warning("Please enter a valid symbol.")

def correlation():
    st.title("Correlation Analysis")
    symbol = st.text_input("Enter the symbol of the cryptocurrency (e.g., BTC)")
    if st.button("Get Correlation"):
        if symbol:
            correlation_data = get_correlation_data(symbol)
            if correlation_data:
                st.write("Top 10 Correlations:")
                correlation_table = create_correlation_table(correlation_data)
                st.dataframe(correlation_table)
            else:
                st.error("Failed to load correlation data.")


# Definir un diccionario que mapea nombres de página a funciones de página
pages = {"Home": home, "Price Prediction": price_prediction, "Correlation": correlation}


# Barra lateral para la navegación entre páginas
page = st.sidebar.selectbox("Select a page", tuple(pages.keys()))

# Ejecuta la función de la página seleccionada
pages[page]()
