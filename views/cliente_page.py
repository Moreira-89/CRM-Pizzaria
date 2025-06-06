import streamlit as st
from dao.cliente_dao import ClienteDAO
from models.cliente import Cliente
from views.utils import buscar_por_campo_unico

def cliente_page():
    st.title("Gestão de Clientes")
    cliente_dao = ClienteDAO()
    menu = ["Cadastrar", "Listar", "Atualizar", "Deletar"]
    escolha = st.sidebar.selectbox("Ações", menu)

    if escolha == "Cadastrar":
        st.subheader("Cadastrar Novo Cliente")
        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF/CNPJ")
        email = st.text_input("E-mail")
        telefone = st.text_input("Telefone")
        endereco = st.text_input("Endereço Completo")
        sms = st.checkbox("Opt-in SMS")
        email_opt = st.checkbox("Opt-in E-mail")
        whatsapp = st.checkbox("Opt-in WhatsApp")
        preferencias = st.text_input("Preferências (separe por vírgula)")
        if st.button("Salvar"):
            cliente = Cliente(
                id=None,
                nome=nome,
                cpf=cpf,
                email=email,
                telefone=telefone,
                endereco=endereco,
                preferencias=[p.strip() for p in preferencias.split(",")] if preferencias else [],
                opt_in={"sms": sms, "email": email_opt, "whatsapp": whatsapp}
            )
            cliente_dao.criar(cliente)
            st.success(f"Cliente {nome} cadastrado com sucesso!")

    elif escolha == "Listar":
        st.subheader("Lista de Clientes")
        clientes = cliente_dao.listar_todos()
        for cliente in clientes:
            st.markdown(f"**ID:** {cliente.id}")
            st.markdown(f"**Nome:** {cliente.nome}")
            st.markdown(f"**CPF/CNPJ:** {cliente.cpf}")
            st.markdown(f"**E-mail:** {cliente.email}")
            st.markdown(f"**Telefone:** {cliente.telefone}")
            st.markdown(f"**Endereço:** {cliente.endereco}")
            st.markdown("---")

    elif escolha == "Atualizar":
        st.subheader("Atualizar Cliente")
        cpf = st.text_input("CPF")
        telefone = st.text_input("Telefone")
        nome_busca = st.text_input("Nome Completo")
        if st.button("Buscar"):
            cliente, erro = buscar_por_campo_unico(cliente_dao, cpf=cpf, telefone=telefone, nome=nome_busca)
            if cliente:
                nome = st.text_input("Nome Completo", cliente.nome)
                telefone = st.text_input("Telefone", cliente.telefone)
                endereco = st.text_input("Endereço", cliente.endereco)
                if st.button("Atualizar"):
                    cliente.nome = nome
                    cliente.telefone = telefone
                    cliente.endereco = endereco
                    cliente_dao.atualizar(cliente)
                    st.success("Cliente atualizado com sucesso!")
            else:
                st.error(erro)

    elif escolha == "Deletar":
        st.subheader("Deletar Cliente")
        cpf = st.text_input("CPF")
        telefone = st.text_input("Telefone")
        nome_busca = st.text_input("Nome Completo")
        if st.button("Buscar"):
            cliente, erro = buscar_por_campo_unico(cliente_dao, cpf=cpf, telefone=telefone, nome=nome_busca)
            if cliente:
                if st.button("Confirmar Exclusão"):
                    cliente_dao.deletar(cliente.id)
                    st.success("Cliente deletado com sucesso!")
            else:
                st.error(erro)