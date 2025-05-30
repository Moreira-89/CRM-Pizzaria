import streamlit as st
from views.cliente_page import cliente_page
from views.motoboy_page import motoboy_page

# Futuramente, importar outras páginas:
#from views.avaliacao_page import avaliacao_page
# from views.fidelidade_page import fidelidade_page
# from views.campanha_page import campanha_page


st.set_page_config(
    page_title="CRM Pizzaria",
    layout="wide"
)

#Barra lateral
st.sidebar.image("https://img.freepik.com/free-vector/pizza-logo-design_23-2149423871.jpg", width=150)
st.sidebar.title("CRM Pizzaria Delivery")

menu = ["Clientes", "Motoboys"]
escolha = st.sidebar.selectbox("Menu Principal", menu)

if escolha == "Clientes":
    cliente_page()
elif escolha == "Motoboys":
    motoboy_page()

st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido por Amanda Taveira Amorim")
