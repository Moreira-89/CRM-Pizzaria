import streamlit as st
from dao.cliente_dao import ClienteDAO
from dao.motoboy_dao import MotoboyDAO
from dao.avaliacao_dao import AvaliacaoDAO
from dao.fidelidade_dao import FidelidadeDAO
from dao.campanha_dao import CampanhaDAO
from datetime import datetime


def dashboard_page():
    st.title("📊 Dashboard Geral da Operação")

    #Instanciar DAOs
    cliente_dao = ClienteDAO()
    motoboy_dao = MotoboyDAO()
    avaliacao_dao = AvaliacaoDAO()
    fidelidade_dao = FidelidadeDAO()
    campanha_dao = CampanhaDAO()

    #Carregar dados
    clientes = cliente_dao.listar_todos()
    motoboys = motoboy_dao.listar_todos()
    avaliacoes = avaliacao_dao.listar_todos()
    fidelidades = fidelidade_dao.listar_todos()
    campanhas = campanha_dao.listar_todos()

    st.subheader("📌 Visão Geral")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Clientes Cadastrados", len(clientes))

    with col2:
        st.metric("Motoboys Ativos", len([m for m in motoboys if m.status_operacional.lower() == "online"]))

    with col3:
        st.metric("Total de Campanhas", len(campanhas))

    col4, col5 = st.columns(2)

    with col4:
        st.metric("Total de Avaliações", len(avaliacoes))

    with col5:
        st.metric("Clientes com Fidelidade", len(fidelidades))

    st.divider()

    #Avaliações
    st.subheader("⭐ Avaliações — Média Geral")

    if avaliacoes:
        notas = [a.nota for a in avaliacoes]
        media = sum(notas) / len(notas)
        st.metric("Média Geral de Avaliações", f"{media:.2f}")

        dist = {str(nota): notas.count(nota) for nota in range(1, 6)}
        st.bar_chart(dist)
    else:
        st.info("Nenhuma avaliação cadastrada.")

    st.divider()

    #Fidelidade
    st.subheader("🏆 Fidelidade — Distribuição por Nível")
    niveis = {"bronze": 0, "prata": 0, "ouro": 0}

    for f in fidelidades:
        if f.nivel.lower() in niveis:
            niveis[f.nivel.lower()] += 1

    st.bar_chart(niveis)

    st.divider()

    #Campanhas
    st.subheader("📣 Desempenho das Campanhas")

    if campanhas:
        campanhas_dict = {c.nome: c.clientes_atingidos for c in campanhas}
        st.bar_chart(campanhas_dict)

        col6, col7 = st.columns(2)

        medias_resposta = sum(c.taxa_resposta for c in campanhas) / len(campanhas)
        medias_conversao = sum(c.conversao for c in campanhas) / len(campanhas)

        with col6:
            st.metric("Média de Taxa de Resposta", f"{medias_resposta:.2f}%")

        with col7:
            st.metric("Média de Conversão", f"{medias_conversao:.2f}%")
    else:
        st.info("Nenhuma campanha cadastrada.")

    st.divider()

    #Atividade dos Motoboys
    st.subheader("🏍️ Status dos Motoboys")
    status = {"Online": 0, "Offline": 0}

    for m in motoboys:
        if m.status_operacional.lower() == "online":
            status["Online"] += 1
        else:
            status["Offline"] += 1

    st.bar_chart(status)

    st.divider()

    #Detalhes finais
    with st.expander("📄 Ver Detalhes de Campanhas"):
        for c in campanhas:
            st.markdown(f"**Nome:** {c.nome}")
            st.markdown(f"**Período:** {c.data_inicio} até {c.data_fim}")
            st.markdown(f"**Canais:** {', '.join(c.canais)}")
            st.markdown(f"**Público:** {', '.join(c.publicos_segmentados)}")
            st.markdown(f"**Clientes Atingidos:** {c.clientes_atingidos}")
            st.markdown(f"**Taxa de Resposta:** {c.taxa_resposta}%")
            st.markdown(f"**Conversão:** {c.conversao}%")
            st.markdown(f"**ROI:** {c.roi}")
            st.markdown("---")
