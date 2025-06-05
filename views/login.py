import streamlit as st

def login_view():
     st.title("🍕 CRM Pizzaria - Login")

        with st.form("login_form"):
            nome = st.text_input("Seu nome")
            perfil = st.selectbox(
                "Selecione seu perfil",
                ["Funcionário", "Motoboy", "Cliente"]
            )
            submit = st.form_submit_button("Entrar")

        if submit:
            if nome.strip() == "":
                st.error("Por favor, preencha seu nome.")
                st.stop()

            # Salva na sessão
            st.session_state["usuario_nome"] = nome
            st.session_state["usuario_perfil"] = perfil
            st.session_state["logado"] = True
            st.success(f"Bem-vindo, {nome}! Você está logado como {perfil}.")