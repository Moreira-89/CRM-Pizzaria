import streamlit as st
from models.motoboy import Motoboy
from dao.motoboy_dao import MotoboyDAO


def motoboy_page():
    st.title("Gestão de Motoboys")

    motoboy_dao = MotoboyDAO()

    menu = ["Cadastrar", "Listar", "Atualizar", "Deletar"]
    escolha = st.sidebar.selectbox("Ações", menu)

    if escolha == "Cadastrar":
        st.subheader("Cadastrar Novo Motoboy")

        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF")
        cnh = st.text_input("Número da CNH")
        telefone = st.text_input("Telefone")
        status = st.selectbox("Status Operacional", ["Online", "Offline"])

        zonas = st.text_input("Zonas de Atuação (separe por vírgula)")
        horarios = st.text_input("Horários Disponíveis (ex.: Seg a Sex 18h-23h)")

        if st.button("Salvar"):
            motoboy = Motoboy(
                id=None,
                nome=nome,
                cpf=cpf,
                cnh=cnh,
                telefone=telefone,
                status_operacional=status,
                zonas_atuacao=[z.strip() for z in zonas.split(",")] if zonas else [],
                horarios_disponiveis=[h.strip() for h in horarios.split(",")] if horarios else [],
            )
            motoboy_dao.criar(motoboy)
            st.success(f"Motoboy {nome} cadastrado com sucesso!")

    elif escolha == "Listar":
        st.subheader("Lista de Motoboys")
        motoboys = motoboy_dao.listar_todos()

        for m in motoboys:
            st.markdown(f"**ID:** {m.id}")
            st.markdown(f"**Nome:** {m.nome}")
            st.markdown(f"**CPF:** {m.cpf}")
            st.markdown(f"**CNH:** {m.cnh}")
            st.markdown(f"**Telefone:** {m.telefone}")
            st.markdown(f"**Status:** {m.status_operacional}")
            st.markdown(f"**Zonas:** {', '.join(m.zonas_atuacao)}")
            st.markdown(f"**Horários:** {', '.join(m.horarios_disponiveis)}")
            st.markdown("---")

    elif escolha == "Atualizar":
        st.subheader("Atualizar Motoboy")
        id_motoboy = st.text_input("ID do Motoboy")

        if st.button("Buscar"):
            m = motoboy_dao.buscar_por_id(id_motoboy)
            if m:
                nome = st.text_input("Nome Completo", m.nome)
                telefone = st.text_input("Telefone", m.telefone)
                status = st.selectbox("Status Operacional", ["Online", "Offline"], index=0 if m.status_operacional == "Online" else 1)

                if st.button("Atualizar"):
                    m.nome = nome
                    m.telefone = telefone
                    m.status_operacional = status
                    motoboy_dao.atualizar(m)
                    st.success("Motoboy atualizado com sucesso!")
            else:
                st.error("Motoboy não encontrado.")

    elif escolha == "Deletar":
        st.subheader("Deletar Motoboy")
        id_motoboy = st.text_input("ID do Motoboy")

        if st.button("Deletar"):
            m = motoboy_dao.buscar_por_id(id_motoboy)
            if m:
                motoboy_dao.deletar(id_motoboy)
                st.success("Motoboy deletado com sucesso!")
            else:
                st.error("Motoboy não encontrado.")
