import streamlit as st
from views.cliente_page import cliente_page
from views.motoboy_page import motoboy_page
from views.avaliacao_page import avaliacao_page

# Futuramente, importar outras páginas:
# from views.fidelidade_page import fidelidade_page
# from views.campanha_page import campanha_page


st.set_page_config(
    page_title="CRM Pizzaria",
    layout="wide"
)

#Barra lateral
st.sidebar.image("https://br.vexels.com/png-svg/previsualizar/190242/pizza-plana-kawaii.png", width=150)
st.sidebar.title("CRM Pizzaria Delivery")

menu = ["Clientes", "Motoboys", "Avaliações"]
escolha = st.sidebar.selectbox("Menu Principal", menu)

if escolha == "Clientes":
    cliente_page()
elif escolha == "Motoboys":
    motoboy_page()
elif escolha == "Avaliações":
    avaliacao_page()

st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido por Amanda Taveira Amorim")
