import streamlit as st
from models.campanha import Campanha
from dao.campanha_dao import CampanhaDAO
from datetime import datetime


def campanha_page():
    st.title("Gestão de Campanhas de Marketing")

    campanha_dao = CampanhaDAO()

    menu = ["Cadastrar", "Listar", "Atualizar", "Deletar"]
    escolha = st.sidebar.selectbox("Menu Campanha", menu)

    if escolha == "Cadastrar":
        st.subheader("Cadastrar Nova Campanha")

        nome = st.text_input("Nome da Campanha")
        objetivo = st.text_area("Objetivo da Campanha")
        data_inicio = st.date_input("Data de Início").strftime("%Y-%m-%d")
        data_fim = st.date_input("Data de Fim").strftime("%Y-%m-%d")

        canais = st.multiselect(
            "Canais",
            ["email", "whatsapp", "sms"]
        )

        publicos_segmentados = st.text_input(
            "Segmentação de Público (Ex.: frequentes, Suzano, inativos)"
        )

        if st.button("Salvar"):
            campanha = Campanha(
                id=None,
                nome=nome,
                objetivo=objetivo,
                data_inicio=data_inicio,
                data_fim=data_fim,
                canais=canais,
                publicos_segmentados=[p.strip() for p in publicos_segmentados.split(",")] if publicos_segmentados else [],
                clientes_atingidos=0,
                taxa_resposta=0.0,
                conversao=0.0,
                roi=0.0
            )
            campanha_dao.criar(campanha)
            st.success("Campanha cadastrada com sucesso!")

    elif escolha == "Listar":
        st.subheader("Lista de Campanhas")
        campanhas = campanha_dao.listar_todos()

        for c in campanhas:
            st.markdown(f"**ID:** {c.id}")
            st.markdown(f"**Nome:** {c.nome}")
            st.markdown(f"**Objetivo:** {c.objetivo}")
            st.markdown(f"**Período:** {c.data_inicio} até {c.data_fim}")
            st.markdown(f"**Canais:** {', '.join(c.canais)}")
            st.markdown(f"**Público Segmentado:** {', '.join(c.publicos_segmentados)}")
            st.markdown(f"**Clientes Atingidos:** {c.clientes_atingidos}")
            st.markdown(f"**Taxa de Resposta:** {c.taxa_resposta}%")
            st.markdown(f"**Conversão:** {c.conversao}%")
            st.markdown(f"**ROI:** {c.roi}")
            st.markdown(f"**Data de Criação:** {c.data_criacao}")
            st.markdown("---")

    elif escolha == "Atualizar":
        st.subheader("Atualizar Campanha")
        id_campanha = st.text_input("ID da Campanha")

        if st.button("Buscar"):
            c = campanha_dao.buscar_por_id(id_campanha)
            if c:
                clientes_atingidos = st.number_input("Clientes Atingidos", min_value=0, step=1, value=c.clientes_atingidos)
                taxa_resposta = st.number_input("Taxa de Resposta (%)", min_value=0.0, max_value=100.0, step=0.1, value=c.taxa_resposta)
                conversao = st.number_input("Conversão (%)", min_value=0.0, max_value=100.0, step=0.1, value=c.conversao)
                roi = st.number_input("ROI (Retorno sobre Investimento)", step=0.1, value=c.roi)

                if st.button("Atualizar"):
                    c.clientes_atingidos = clientes_atingidos
                    c.taxa_resposta = taxa_resposta
                    c.conversao = conversao
                    c.roi = roi
                    campanha_dao.atualizar(c)
                    st.success("Campanha atualizada com sucesso!")
            else:
                st.error("Campanha não encontrada.")

    elif escolha == "Deletar":
        st.subheader("Deletar Campanha")
        id_campanha = st.text_input("ID da Campanha")

        if st.button("Deletar"):
            c = campanha_dao.buscar_por_id(id_campanha)
            if c:
                campanha_dao.deletar(id_campanha)
                st.success("Campanha deletada com sucesso!")
            else:
                st.error("Campanha não encontrada.")
