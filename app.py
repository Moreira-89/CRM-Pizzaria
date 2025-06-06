import streamlit as st

from views.cliente_page import cliente_page
from views.motoboy_page import motoboy_page
from views.avaliacao_page import avaliacao_page

def login():
    st.title("Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        # Simulação de autenticação
        if usuario == "admin" and senha == "admin":
            st.session_state["logado"] = True
            st.session_state["usuario_nome"] = "Administrador"
            st.session_state["usuario_perfil"] = "Funcionário"
        elif usuario == "motoboy" and senha == "123":
            st.session_state["logado"] = True
            st.session_state["usuario_nome"] = "Motoboy XPTO"
            st.session_state["usuario_perfil"] = "Motoboy"
        elif usuario == "cliente" and senha == "abc":
            st.session_state["logado"] = True
            st.session_state["usuario_nome"] = "Cliente XPTO"
            st.session_state["usuario_perfil"] = "Cliente"
        else:
            st.error("Usuário ou senha inválidos")
        st.rerun()

if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login()
else:
    perfil = st.session_state["usuario_perfil"]
    nome = st.session_state["usuario_nome"]

    st.sidebar.image(
        "https://img.freepik.com/free-vector/pizza-logo-design_23-2149423871.jpg",
        width=150
    )
    st.sidebar.title(f"🍕 Bem-vindo, {nome} ({perfil})")

    # Menu e páginas conforme perfil
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
            from views.dashboard_page import dashboard_page
            dashboard_page()
        elif escolha == "Clientes":
            cliente_page()
        elif escolha == "Motoboys":
            motoboy_page()
        elif escolha == "Avaliações 360°":
            avaliacao_page(perfil=perfil, usuario=nome)
        elif escolha == "Fidelidade":
            from views.fidelidade_page import fidelidade_page
            fidelidade_page()
        elif escolha == "Campanhas":
            from views.campanha_page import campanha_page
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
        elif escolha == "Avaliar Pedido":
            avaliacao_page(perfil=perfil, usuario=nome, modo="avaliar_pedido")
        elif escolha == "Sair":
            st.session_state.clear()
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("Desenvolvido por Amanda Taveira Amorim")
    st.sidebar.markdown("Versão 1.0 - 2025")