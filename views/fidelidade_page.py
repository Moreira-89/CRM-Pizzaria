import streamlit as st
from models.fidelidade import Fidelidade
from dao.fidelidade_dao import FidelidadeDAO
from dao.cliente_dao import ClienteDAO
from datetime import datetime


def fidelidade_page():
    st.title("Gestão do Programa de Fidelidade")

    fidelidade_dao = FidelidadeDAO()
    cliente_dao = ClienteDAO()

    menu = ["Cadastrar", "Listar", "Atualizar", "Deletar"]
    escolha = st.sidebar.selectbox("Menu Fidelidade", menu)

    if escolha == "Cadastrar":
        st.subheader("Cadastrar Fidelidade para Cliente")

        nome_cliente = st.text_input("Nome do Cliente")
        pontos = st.number_input("Pontos", min_value=0, step=1)
        nivel = st.selectbox("Nível", ["bronze", "prata", "ouro"])
        validade = st.date_input("Validade dos Pontos").strftime("%Y-%m-%d")

        if st.button("Buscar Cliente"):
            cliente = cliente_dao.buscar_por_nome(nome_cliente)
            if cliente:
                st.success(f"Cliente encontrado: {cliente['nome']} (ID: {cliente['id']})")
                cliente_id = cliente["id"]

                if st.button("Salvar"):
                    fidelidade = Fidelidade(
                        id=None,
                        cliente_id=cliente_id,
                        cliente_nome=cliente["nome"],
                        pontos=pontos,
                        nivel=nivel,
                        validade=validade,
                        historico=[]
                    )
                    fidelidade_dao.criar(fidelidade)
                    st.success("Fidelidade cadastrada com sucesso!")
            else:
                st.error("Cliente não encontrado.")

    elif escolha == "Listar":
        st.subheader("Lista de Programas de Fidelidade")
        registros = fidelidade_dao.listar_todos()

        for f in registros:
            st.markdown(f"**ID:** {f.id}")
            st.markdown(f"**Cliente:** {f.cliente_nome} (ID: {f.cliente_id})")
            st.markdown(f"**Pontos:** {f.pontos}")
            st.markdown(f"**Nível:** {f.nivel}")
            st.markdown(f"**Validade:** {f.validade}")
            st.markdown(f"**Histórico:** {f.historico}")
            st.markdown("---")

    elif escolha == "Atualizar":
        st.subheader("Atualizar Fidelidade")
        id_fidelidade = st.text_input("ID da Fidelidade")

        if st.button("Buscar"):
            f = fidelidade_dao.buscar_por_id(id_fidelidade)
            if f:
                pontos = st.number_input("Pontos", min_value=0, step=1, value=f.pontos)
                nivel = st.selectbox("Nível", ["bronze", "prata", "ouro"], index=["bronze", "prata", "ouro"].index(f.nivel))
                validade = st.date_input("Validade dos Pontos", value=datetime.strptime(f.validade, "%Y-%m-%d")).strftime("%Y-%m-%d")

                if st.button("Atualizar"):
                    f.pontos = pontos
                    f.nivel = nivel
                    f.validade = validade
                    fidelidade_dao.atualizar(f)
                    st.success("Fidelidade atualizada com sucesso!")
            else:
                st.error("Registro de fidelidade não encontrado.")

    elif escolha == "Deletar":
        st.subheader("Deletar Fidelidade")
        id_fidelidade = st.text_input("ID da Fidelidade")

        if st.button("Deletar"):
            f = fidelidade_dao.buscar_por_id(id_fidelidade)
            if f:
                fidelidade_dao.deletar(id_fidelidade)
                st.success("Fidelidade deletada com sucesso!")
            else:
                st.error("Registro não encontrado.")
