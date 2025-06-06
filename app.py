import streamlit as st
from views.cliente_page import cliente_page
from views.motoboy_page import motoboy_page
from views.avaliacao_page import avaliacao_page
from views.dashboard_page import dashboard_page
from views.fidelidade_page import fidelidade_page
from views.campanha_page import campanha_page
from views.register_page import register_page
from dao.usuario_dao import UsuarioDAO


def configurar_pagina():
    st.set_page_config(
        page_title="Sistema de Gestão - Pizzaria",
        page_icon="🍕"
    )

def tela_login():
    configurar_pagina()

    st.markdown("### 🔐 Login")

    if st.session_state.get("cadastrar", False):
        register_page()
        return

    login_id = st.text_input("ID ou E-mail")
    senha = st.text_input("Senha", type="password")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Entrar"):
            usuario_dao = UsuarioDAO()
            if usuario_dao.autenticar(login_id.strip(), senha.strip()):
                usuario = usuario_dao.buscar_por_id(login_id.strip())
                if usuario:
                    st.session_state["logado"] = True
                    st.session_state["usuario_nome"] = usuario.nome
                    st.session_state["usuario_perfil"] = usuario.perfil
                    st.session_state["usuario_id"] = usuario.id
                    st.rerun()
                else:
                    st.error("Falha ao obter dados de usuário após autenticar.")
            else:
                st.error("Usuário ou senha inválidos.")
    with col2:
        if st.button("Cadastrar Cliente"):
            st.session_state["cadastrar"] = True
            st.rerun()


# Inicializa estado de sessão
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if "cadastrar" not in st.session_state:
    st.session_state["cadastrar"] = False

# Se não estiver logado, exibe tela de login/registro
if not st.session_state["logado"]:
    tela_login()
    st.stop()  # evita mostrar o resto da página antes de logar

# Se chegou aqui, é porque o usuário está logado
perfil = st.session_state["usuario_perfil"]
nome = st.session_state["usuario_nome"]

# Barra lateral fixa, depois de logar
st.sidebar.image(
    "https://img.freepik.com/free-vector/pizza-logo-design_23-2149423871.jpg",
    width=150
)
st.sidebar.title(f"🍕 Bem-vindo, {nome} ({perfil})")

# Monta menu conforme perfil
if perfil == "Funcionário":
    menu = [
        "Dashboard Geral",
        "Clientes",
        "Motoboys",
        "Avaliações 360°",
        "Fidelidade",
        "Campanhas",
        "Sair"
    ]
    escolha = st.sidebar.selectbox("Menu Principal", menu)
    if escolha == "Dashboard Geral":
        dashboard_page()
    elif escolha == "Clientes":
        cliente_page()
    elif escolha == "Motoboys":
        motoboy_page()
    elif escolha == "Avaliações 360°":
        avaliacao_page(perfil=perfil, usuario=nome)
    elif escolha == "Fidelidade":
        fidelidade_page()
    elif escolha == "Campanhas":
        campanha_page()
    elif escolha == "Sair":
        st.session_state.clear()
        st.rerun()

elif perfil == "Motoboy":
    menu = [
        "Avaliar Cliente",
        "Minhas Avaliações",
        "Sair"
    ]
    escolha = st.sidebar.selectbox("Menu Principal", menu)
    if escolha == "Avaliar Cliente":
        avaliacao_page(perfil=perfil, usuario=nome, modo="avaliar_cliente")
    elif escolha == "Minhas Avaliações":
        avaliacao_page(perfil=perfil, usuario=nome, modo="minhas_avaliacoes")
    elif escolha == "Sair":
        st.session_state.clear()
        st.rerun()

elif perfil == "Cliente":
    menu = [
        "Avaliar Pizzaria",
        "Avaliar Motoboy",
        "Sair"
    ]
    escolha = st.sidebar.selectbox("Menu Principal", menu)
    if escolha == "Avaliar Pizzaria":
        avaliacao_page(perfil=perfil, usuario=nome, modo="avaliar_pizzaria")
    elif escolha == "Avaliar Motoboy":
        avaliacao_page(perfil=perfil, usuario=nome, modo="avaliar_motoboy")
    elif escolha == "Sair":
        st.session_state.clear()
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido por Amanda Taveira Amorim")
st.sidebar.markdown("Versão 1.0 - 2025")
