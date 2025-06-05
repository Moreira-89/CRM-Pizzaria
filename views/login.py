import streamlit as st
from dao.usuario_dao import UsuarioDAO


def login_page():
    st.title("🍕 CRM Pizzaria - Login")

    usuario_dao = UsuarioDAO()

    with st.form("login_form"):
        nome = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")

    if submit:
        if nome.strip() == "" or senha.strip() == "":
            st.error("Por favor, preencha usuário e senha.")
            st.stop()

        usuario = usuario_dao.buscar_por_nome(nome)

        if usuario and usuario.validar_senha(senha):
            st.session_state["usuario_nome"] = usuario.nome
            st.session_state["usuario_perfil"] = usuario.perfil
            st.session_state["logado"] = True
            st.success(f"Bem-vindo, {usuario.nome} ({usuario.perfil})")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos.")
