import streamlit as st
from dao.motoboy_dao import MotoboyDAO
from models.motoboy import Motoboy
from views.utils import buscar_por_campo_unico


def motoboy_page():
    st.title("Gestão de Entregadores")
    motoboy_dao = MotoboyDAO()
    menu = ["Cadastrar", "Listar", "Atualizar", "Deletar"]
    escolha = st.sidebar.selectbox("Ações", menu)

    if escolha == "Cadastrar":
        st.subheader("Cadastrar novo entregador")
        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF")
        cnh = st.text_input("CNH")
        telefone = st.text_input("Telefone")
        status = st.selectbox("Status Operacional", ["Ativo", "Inativo", "Pausado", "Em Entrega"])
        zonas = st.text_input("Zonas de Atuação (separe por vírgula)")
        horarios = st.text_input("Horários Disponíveis (separe por vírgula)")
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
            st.success(f"Entregador {nome} cadastrado com sucesso!")

    elif escolha == "Listar":
        st.subheader("Lista de Entregadores")
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
        st.subheader("Atualizar Entregador")
        cpf = st.text_input("CPF")
        telefone = st.text_input("Telefone")
        nome_busca = st.text_input("Nome Completo")
        if st.button("Buscar"):
            m, erro = buscar_por_campo_unico(motoboy_dao, cpf=cpf, telefone=telefone, nome=nome_busca)
            if m:
                nome = st.text_input("Nome Completo", m.nome)
                telefone = st.text_input("Telefone", m.telefone)
                status = st.selectbox("Status Operacional", ["Ativo", "Inativo", "Pausado", "Em Entrega"], index=0 if m.status_operacional == "Online" else 1)
                if st.button("Atualizar"):
                    m.nome = nome
                    m.telefone = telefone
                    m.status_operacional = status
                    motoboy_dao.atualizar(m)
                    st.success("Entregador atualizado com sucesso!")
            else:
                st.error(erro)

    elif escolha == "Deletar":
        st.subheader("Deletar Entregador")
        cpf = st.text_input("CPF")
        telefone = st.text_input("Telefone")
        nome_busca = st.text_input("Nome Completo")
        if st.button("Buscar"):
            m, erro = buscar_por_campo_unico(motoboy_dao, cpf=cpf, telefone=telefone, nome=nome_busca)
            if m:
                if st.button("Confirmar Exclusão"):
                    motoboy_dao.deletar(m.id)
                    st.success("Entregador deletado com sucesso!")
            else:
                st.error(erro)