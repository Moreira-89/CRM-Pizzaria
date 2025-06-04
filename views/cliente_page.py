import streamlit as st
from models.cliente import Cliente
from dao.cliente_dao import ClienteDAO


def cliente_page():
    st.title("Gestão de Clientes")

    cliente_dao = ClienteDAO()

    menu = ["Cadastrar", "Listar", "Atualizar", "Deletar"]
    escolha = st.sidebar.selectbox("Ações", menu)

    if escolha == "Cadastrar":
        st.subheader("Cadastrar Novo Cliente")

        nome = st.text_input("Nome Completo")
        cpf_cnpj = st.text_input("CPF/CNPJ")
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
                cpf_cnpj=cpf_cnpj,
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
            st.markdown(f"**CPF/CNPJ:** {cliente.cpf_cnpj}")
            st.markdown(f"**E-mail:** {cliente.email}")
            st.markdown(f"**Telefone:** {cliente.telefone}")
            st.markdown(f"**Endereço:** {cliente.endereco}")
            st.markdown("---")

    elif escolha == "Atualizar":
        st.subheader("Atualizar Cliente")
        id_cliente = st.text_input("ID do Cliente")

        if st.button("Buscar"):
            cliente = cliente_dao.buscar_por_id(id_cliente)
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
                st.error("Cliente não encontrado.")

    elif escolha == "Deletar":
        st.subheader("Deletar Cliente")
        id_cliente = st.text_input("ID do Cliente")

        if st.button("Deletar"):
            cliente = cliente_dao.buscar_por_id(id_cliente)
            if cliente:
                cliente_dao.deletar(id_cliente)
                st.success("Cliente deletado com sucesso!")
            else:
                st.error("Cliente não encontrado.")
