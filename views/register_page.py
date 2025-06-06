# views/register_page.py

import streamlit as st
import uuid
from models.usuario import Usuario
from models.cliente import Cliente
from dao.usuario_dao import UsuarioDAO
from dao.cliente_dao import ClienteDAO
from datetime import datetime

def register_page():
    """
    Página de registro para que um novo cliente se cadastre.
    Após criar, redireciona para a tela de login.
    """
    st.markdown("### 📝 Cadastro de Cliente")

    usuario_dao = UsuarioDAO()
    cliente_dao = ClienteDAO()

    with st.form(key="form_cadastro_cliente", clear_on_submit=True):
        nome = st.text_input("Nome Completo*", max_chars=100)
        cpf = st.text_input("CPF*", max_chars=18)
        telefone = st.text_input("Telefone*", max_chars=15)
        email = st.text_input("E-mail (será usado como login)*", max_chars=100)
        endereco = st.text_input("Endereço Completo*", max_chars=200)
        senha = st.text_input("Senha*", type="password", max_chars=50)
        confirmar_senha = st.text_input("Confirme a Senha*", type="password", max_chars=50)
        btn_cadastrar = st.form_submit_button("Cadastrar")

    if btn_cadastrar:
        erros = []

        # Validações básicas
        if not nome.strip():
            erros.append("O campo Nome é obrigatório.")
        if not cpf.strip():
            erros.append("O campo CPF é obrigatório.")
        if not telefone.strip():
            erros.append("O campo Telefone é obrigatório.")
        if not email.strip():
            erros.append("O campo E-mail é obrigatório.")
        if not endereco.strip():
            erros.append("O campo Endereço é obrigatório.")
        if not senha or not confirmar_senha:
            erros.append("Informe a senha e a confirmação.")
        elif senha != confirmar_senha:
            erros.append("As senhas não coincidem.")

        # Verifica duplicação: e-mail ou CPF já cadastrado?
        existente_por_email = cliente_dao.buscar_por_email(email.strip())
        existente_por_cpf = cliente_dao.buscar_por_cpf(cpf.strip())
        if existente_por_email:
            erros.append("Já existe um cliente cadastrado com esse e-mail.")
        if existente_por_cpf:
            erros.append("Já existe um cliente cadastrado com esse CPF.")

        if erros:
            for e in erros:
                st.error(e)
            return

        novo_id = str(uuid.uuid4())

        # 1) Cria Usuario (perfil “Cliente”), com senha já criptografada internamente
        usuario = Usuario(
            id=novo_id,
            nome=nome.strip(),
            perfil="Cliente",
            cpf=cpf.strip(),
            telefone=telefone.strip(),
            senha_plain=senha.strip()
        )
        uid = usuario_dao.criar(usuario)
        if not uid:
            st.error("Falha ao gravar credenciais de login. Tente novamente mais tarde.")
            return

        # 2) Cria Cliente (mesmo ID), com dados pessoais
        cliente = Cliente(
            id=novo_id,
            nome=nome.strip(),
            cpf=cpf.strip(),
            telefone=telefone.strip(),
            email=email.strip(),
            endereco=endereco.strip(),
            preferencias=[],
            opt_in={"sms": False, "email": False, "whatsapp": False}
        )
        cid = cliente_dao.criar(cliente)
        if not cid:
            usuario_dao.deletar(novo_id)
            st.error("Falha ao gravar dados de cliente. Tente novamente mais tarde.")
            return

        st.success("Cadastro realizado com sucesso! Você já pode fazer login.")
        st.info("Clique no botão abaixo para voltar ao login.")

        if st.button("Voltar ao Login"):
            # Para forçar recarregar a página de login
            st.session_state["cadastrar"] = False
            st.experimental_rerun()
