import streamlit as st
from views.cliente_page import cliente_page
# Futuramente, importar outras páginas como motoboy_page, avaliacao_page, etc.

st.set_page_config(
    page_title="CRM Pizzaria",
    layout="wide"
)

st.sidebar.image("https://img.freepik.com/free-vector/pizza-logo-design_23-2149423871.jpg", width=150)
st.sidebar.title("CRM Pizzaria Delivery")

menu = ["Clientes"]
escolha = st.sidebar.selectbox("Menu Principal", menu)

if escolha == "Clientes":
    cliente_page()

st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido por Amanda Taveira Amorim")
