import streamlit as st
from dao.cliente_dao import ClienteDAO
from dao.motoboy_dao import MotoboyDAO
from dao.avaliacao_dao import AvaliacaoDAO
from dao.fidelidade_dao import FidelidadeDAO
from dao.campanha_dao import CampanhaDAO
from datetime import datetime
from functools import lru_cache
import matplotlib.pyplot as plt

@lru_cache(maxsize=1)
def carregar_dados_dashboard():
    cliente_dao = ClienteDAO()
    motoboy_dao = MotoboyDAO()
    avaliacao_dao = AvaliacaoDAO()
    fidelidade_dao = FidelidadeDAO()
    campanha_dao = CampanhaDAO()

    clientes = cliente_dao.listar_todos()
    motoboys = motoboy_dao.listar_todos()
    avaliacoes = avaliacao_dao.listar_todos()
    fidelidades = fidelidade_dao.listar_todos()
    campanhas = campanha_dao.listar_todos()

    return clientes, motoboys, avaliacoes, fidelidades, campanhas

def dashboard_page():
    st.title("📊 Dashboard Geral da Operação")

    clientes, motoboys, avaliacoes, fidelidades, campanhas = carregar_dados_dashboard()

    st.subheader("📌 Visão Geral")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Clientes Cadastrados", len(clientes))
    with col2:
        online = len([m for m in motoboys if getattr(m, "status_operacional", "").lower() == "online"])
        st.metric("Motoboys Online", online)
    with col3:
        st.metric("Total de Campanhas", len(campanhas))

    col4, col5 = st.columns(2)
    with col4:
        st.metric("Total de Avaliações", len(avaliacoes))
    with col5:
        st.metric("Clientes com Fidelidade", len(fidelidades))

    st.markdown("---")
    st.subheader("⭐ Avaliações — Estatísticas")
    if avaliacoes:
        notas = [a.nota for a in avaliacoes if a.nota is not None]
        media = sum(notas) / len(notas)
        st.metric("Média das Notas", f"{media:.2f}")
        # Distribuição de notas
        freq = {str(i): notas.count(i) for i in range(1, 6)}
        fig, ax = plt.subplots()
        ax.bar(freq.keys(), freq.values())
        ax.set_xlabel("Nota")
        ax.set_ylabel("Quantidade")
        ax.set_title("Distribuição de Notas")
        st.pyplot(fig)
    else:
        st.info("Nenhuma avaliação registrada.")

    st.markdown("---")
    st.subheader("🏆 Fidelidade — Distribuição por Nível")
    niveis = {"bronze": 0, "prata": 0, "ouro": 0}
    for f in fidelidades:
        nivel = getattr(f, "nivel", "").lower()
        if nivel in niveis:
            niveis[nivel] += 1
    if any(niveis.values()):
        fig2, ax2 = plt.subplots()
        ax2.bar(niveis.keys(), niveis.values(), color=["#cd7f32", "#c0c0c0", "#ffd700"])
        ax2.set_title("Clientes por Nível de Fidelidade")
        st.pyplot(fig2)
    else:
        st.info("Nenhum programa de fidelidade registrado.")

    st.markdown("---")
    st.subheader("📣 Desempenho das Campanhas")
    if campanhas:
        # Clientes atingidos por campanha
        dados = {c.nome: c.clientes_atingidos for c in campanhas}
        fig3, ax3 = plt.subplots()
        ax3.bar(dados.keys(), dados.values())
        ax3.set_xlabel("Campanha")
        ax3.set_ylabel("Clientes Atingidos")
        ax3.set_title("Clientes Atingidos por Campanha")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig3)

        col6, col7 = st.columns(2)
        with col6:
            medias_resposta = sum(c.taxa_resposta for c in campanhas) / len(campanhas)
            st.metric("Média de Taxa de Resposta", f"{medias_resposta:.2f}%")
        with col7:
            medias_conversao = sum(c.conversao for c in campanhas) / len(campanhas)
            st.metric("Média de Conversão", f"{medias_conversao:.2f}%")
    else:
        st.info("Nenhuma campanha cadastrada.")

    st.markdown("---")
    st.subheader("🏍️ Status dos Motoboys")
    status = {"Online": 0, "Offline": 0}
    for m in motoboys:
        if getattr(m, "status_operacional", "").lower() == "online":
            status["Online"] += 1
        else:
            status["Offline"] += 1
    if any(status.values()):
        fig4, ax4 = plt.subplots()
        ax4.bar(status.keys(), status.values(), color=["green", "red"])
        ax4.set_title("Status Operacional dos Motoboys")
        st.pyplot(fig4)
    else:
        st.info("Nenhum motoboy registrado.")

    st.markdown("---")
    with st.expander("📄 Detalhes de Campanhas"):
        if campanhas:
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
        else:
            st.info("Não há campanhas para detalhar.")
