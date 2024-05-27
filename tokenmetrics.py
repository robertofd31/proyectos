import streamlit as st

# Datos de ejemplo
data = {
  "success": True,
  "message": "Data fetched successfully",
  "length": 1000,
  "data": [
    {
      "TOKEN_ID": 11984,
      "TOKEN_NAME": "Dforce",
      "SYMBOL": "DF",
      "TRADER_REPORT": "## Introduction\n\nThis report provides an analysis of the quantitative metrics for dForce, a cryptocurrency asset, compared to Bitcoin. ...",
      "FUNDAMENTAL_REPORT": None,
      "TECHNOLOGY_REPORT": "## Audit and Security\n\n### Token Audits\nThe dForce token has undergone 1 audit. However, it is crucial to note that the audit is considered outdated, which may not accurately reflect the current state of the technology...."
    },
    # Otros informes podrían estar aquí
  ]
}

# Obtener la lista de tokens y símbolos
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
