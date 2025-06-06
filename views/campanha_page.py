import streamlit as st
from models.campanha import Campanha
from dao.campanha_dao import CampanhaDAO
from datetime import datetime, date

def campanha_page():
    st.title("🎯 Gestão de Campanhas de Marketing")
    campanha_dao = CampanhaDAO()

    menu = ["Cadastrar", "Listar", "Atualizar", "Deletar"]
    escolha = st.sidebar.selectbox("Ações", menu)

    # ======================
    # 1. Cadastrar
    # ======================
    if escolha == "Cadastrar":
        st.subheader("➕ Cadastrar Nova Campanha")
        with st.form(key="form_cadastrar_campanha", clear_on_submit=True):
            nome = st.text_input("Nome da Campanha*", max_chars=100)
            objetivo = st.text_area("Objetivo da Campanha*", max_chars=500)
            data_inicio = st.date_input("Data de Início*", min_value=date.today())
            data_fim = st.date_input("Data de Fim*", min_value=data_inicio)
            canais = st.multiselect(
                "Canais*",
                options=["email", "whatsapp", "sms"]
            )
            publicos_segmentados = st.text_input(
                "Segmentação de Público (ex.: frequentes, Suzano, inativos)",
                max_chars=200
            )
            btn_salvar = st.form_submit_button("Salvar Campanha")

        if btn_salvar:
            erros = []
            if not nome.strip():
                erros.append("O campo Nome é obrigatório.")
            if not objetivo.strip():
                erros.append("O campo Objetivo é obrigatório.")
            if data_fim < data_inicio:
                erros.append("Data de Fim não pode ser anterior à Data de Início.")
            if not canais:
                erros.append("Selecione ao menos um canal.")
            if erros:
                for e in erros:
                    st.error(e)
            else:
                campanha = Campanha(
                    id=None,
                    nome=nome.strip(),
                    objetivo=objetivo.strip(),
                    data_inicio=data_inicio.strftime("%Y-%m-%d"),
                    data_fim=data_fim.strftime("%Y-%m-%d"),
                    canais=canais,
                    publicos_segmentados=[p.strip() for p in publicos_segmentados.split(",")] if publicos_segmentados else [],
                    clientes_atingidos=0,
                    taxa_resposta=0.0,
                    conversao=0.0,
                    roi=0.0,
                    data_criacao=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                ok, msg = campanha_dao.criar(campanha)
                if ok:
                    st.success("Campanha cadastrada com sucesso!")
                else:
                    st.error(f"Erro ao salvar campanha: {msg}")

        return

    # ======================
    # 2. Listar
    # ======================
    if escolha == "Listar":
        st.subheader("📋 Lista de Campanhas")
        campanhas = campanha_dao.listar_todos()
        if not campanhas:
            st.info("Nenhuma campanha cadastrada.")
        else:
            dados = []
            for c in campanhas:
                dados.append({
                    "ID": c.id,
                    "Nome": c.nome,
                    "Objetivo": c.objetivo,
                    "Período": f"{c.data_inicio} até {c.data_fim}",
                    "Canais": ", ".join(c.canais),
                    "Público Segmentado": ", ".join(c.publicos_segmentados),
                    "Clientes Atingidos": c.clientes_atingidos,
                    "Taxa de Resposta (%)": c.taxa_resposta,
                    "Conversão (%)": c.conversao,
                    "ROI": c.roi,
                    "Data de Criação": c.data_criacao
                })
            st.table(dados)

        return

    # ======================
    # 3. Atualizar
    # ======================
    if escolha == "Atualizar":
        st.subheader("✏️ Atualizar Campanha")
        with st.form(key="form_buscar_campanha_atualizar"):
            id_busca = st.text_input("ID da Campanha para buscar*", max_chars=50)
            btn_buscar = st.form_submit_button("Buscar")

        if btn_buscar:
            if not id_busca.strip():
                st.error("Informe o ID da campanha.")
            else:
                campanha = campanha_dao.buscar_por_id(id_busca.strip())
                if not campanha:
                    st.warning("Campanha não encontrada.")
                else:
                    # Exibe formulário de atualização
                    with st.form(key="form_atualizar_campanha", clear_on_submit=False):
                        st.markdown(f"**ID:** {campanha.id}")
                        st.markdown(f"**Nome Atual:** {campanha.nome}")
                        st.markdown(f"**Objetivo Atual:** {campanha.objetivo}")
                        st.markdown(f"**Período Atual:** {campanha.data_inicio} até {campanha.data_fim}")
                        novos_clientes_atingidos = st.number_input(
                            "Clientes Atingidos*", min_value=0, step=1, value=campanha.clientes_atingidos
                        )
                        nova_taxa_resposta = st.number_input(
                            "Taxa de Resposta (%)*", min_value=0.0, max_value=100.0, step=0.1, value=campanha.taxa_resposta
                        )
                        nova_conversao = st.number_input(
                            "Conversão (%)*", min_value=0.0, max_value=100.0, step=0.1, value=campanha.conversao
                        )
                        novo_roi = st.number_input(
                            "ROI*", min_value=0.0, step=0.1, value=campanha.roi
                        )
                        btn_atualizar = st.form_submit_button("Salvar Atualização")

                    if btn_atualizar:
                        campanha.clientes_atingidos = int(novos_clientes_atingidos)
                        campanha.taxa_resposta = float(nova_taxa_resposta)
                        campanha.conversao = float(nova_conversao)
                        campanha.roi = float(novo_roi)
                        campanha.data_atualizacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ok, msg = campanha_dao.atualizar(campanha)
                        if ok:
                            st.success("Campanha atualizada com sucesso!")
                        else:
                            st.error(f"Erro ao atualizar campanha: {msg}")

        return

    # ======================
    # 4. Deletar
    # ======================
    if escolha == "Deletar":
        st.subheader("❌ Deletar Campanha")
        with st.form(key="form_deletar_campanha"):
            id_del = st.text_input("ID da Campanha para deletar*", max_chars=50)
            btn_deletar = st.form_submit_button("Deletar")

        if btn_deletar:
            if not id_del.strip():
                st.error("Informe o ID da campanha.")
            else:
                campanha = campanha_dao.buscar_por_id(id_del.strip())
                if not campanha:
                    st.warning("Campanha não encontrada.")
                else:
                    ok, msg = campanha_dao.deletar(id_del.strip())
                    if ok:
                        st.success("Campanha deletada com sucesso!")
                    else:
                        st.error(f"Erro ao deletar campanha: {msg}")

        return

    st.error("Ação inválida.")