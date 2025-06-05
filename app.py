import streamlit as st

# Importação das views
from views.login import login_view
from views.cliente_page import cliente_page
from views.motoboy_page import motoboy_page
from views.avaliacao_page import avaliacao_page
from views.fidelidade_page import fidelidade_page
from views.campanha_page import campanha_page
from views.dashboard_page import dashboard_page

#from views.cadastro_usuario import cadastro_usuario_page

# Controle de sessão
if "logado" not in st.session_state:
    st.session_state["logado"] = False

# Login
if not st.session_state["logado"]:
    login_view()

else:
    # Dados do usuário logado
    nome = st.session_state["usuario_nome"]
    perfil = st.session_state["usuario_perfil"]

# Sidebar com boas-vindas
st.sidebar.image(
    "https://img.freepik.com/free-vector/pizza-logo-design_23-2149423871.jpg",
    width=150
)
st.sidebar.title(f"🍕 Bem-vindo, {nome} ({perfil})")

#  Menus dinâmicos conforme perfil
if perfil == "Funcionário":
    menu = [
        "Dashboard Geral",
        "Clientes",
        "Motoboys",
        "Avaliações 360°",
        "Fidelidade",
        "Campanhas",
        "Cadastro de Usuário",  # (opcional interno)
        "Sair"
    ]
elif perfil == "Motoboy":
    menu = ["Avaliações 360°", "Sair"]
elif perfil == "Cliente":
    menu = ["Avaliações 360°", "Sair"]
else:
    menu = ["Sair"]

# Sidebar do menu
escolha = st.sidebar.selectbox("Menu Principal", menu)

#  Roteamento
if escolha == "Dashboard Geral":
    dashboard_page()

elif escolha == "Clientes":
    cliente_page()

elif escolha == "Motoboys":
    motoboy_page()

elif escolha == "Avaliações 360°":
    avaliacao_page()

elif escolha == "Fidelidade":
    fidelidade_page()

elif escolha == "Campanhas":
    campanha_page()

#elif escolha == "Cadastro de Usuário":
#    cadastro_usuario_page()

elif escolha == "Sair":
    st.session_state["logado"] = False
    st.session_state["usuario_nome"] = None
    st.session_state["usuario_perfil"] = None
    st.experimental_rerun()

# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido por Amanda Taveira Amorim")
st.sidebar.markdown("Versão 1.0 - 2025")