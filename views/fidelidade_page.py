import streamlit as st
from models.fidelidade import Fidelidade
from dao.fidelidade_dao import FidelidadeDAO
from dao.cliente_dao import ClienteDAO
from datetime import datetime, date

def fidelidade_page():
    st.markdown("### 🎁 Gestão do Programa de Fidelidade")
    fidelidade_dao = FidelidadeDAO()
    cliente_dao = ClienteDAO()

    menu = ["Cadastrar", "Listar", "Atualizar", "Deletar"]
    escolha = st.sidebar.selectbox("Ações (Fidelidade)", menu)

    # ======================
    # 1. Cadastrar
    # ======================
    if escolha == "Cadastrar":
        st.subheader("➕ Cadastrar Programa de Fidelidade")
        with st.form(key="form_cadastrar_fidelidade", clear_on_submit=True):
            nome_cliente = st.text_input("Nome do Cliente*", max_chars=100)
            pontos = st.number_input("Pontos*", min_value=0, step=1)
            nivel = st.selectbox("Nível*", ["bronze", "prata", "ouro"])
            validade = st.date_input("Data de Validade*", min_value=date.today())
            btn_salvar = st.form_submit_button("Salvar")

        if btn_salvar:
            if not nome_cliente.strip():
                st.error("Informe o nome do cliente.")
            else:
                cliente = cliente_dao.buscar_por_nome(nome_cliente.strip())
                if not cliente:
                    st.error("Cliente não encontrado.")
                else:
                    fidelidade = Fidelidade(
                        id=None,
                        cliente_id=cliente["id"],
                        cliente_nome=cliente["nome"],
                        pontos=int(pontos),
                        nivel=nivel,
                        validade=validade.strftime("%Y-%m-%d"),
                        historico=[],
                        data_criacao=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    ok, msg = fidelidade_dao.criar(fidelidade)
                    if ok:
                        st.success("Programa de fidelidade cadastrado com sucesso!")
                    else:
                        st.error(f"Erro ao cadastrar fidelidade: {msg}")

        return

    # ======================
    # 2. Listar
    # ======================
    if escolha == "Listar":
        st.subheader("📋 Lista de Programas de Fidelidade")
        registros = fidelidade_dao.listar_todos()
        if not registros:
            st.info("Nenhum programa cadastrado.")
        else:
            dados = []
            for f in registros:
                status = "Ativo" if datetime.strptime(f.validade, "%Y-%m-%d").date() >= date.today() else "Expirado"
                dados.append({
                    "ID": f.id,
                    "Cliente": f"{f.cliente_nome} (ID: {f.cliente_id})",
                    "Pontos": f.pontos,
                    "Nível": f.nivel.title(),
                    "Validade": f.validade,
                    "Status": status,
                    "Histórico": ", ".join(f.historico) if f.historico else ""
                })
            st.table(dados)

        return

    # ======================
    # 3. Atualizar
    # ======================
    if escolha == "Atualizar":
        st.subheader("✏️ Atualizar Programa de Fidelidade")
        with st.form(key="form_buscar_fidelidade"):
            id_busca = st.text_input("ID do Programa para buscar*", max_chars=50)
            btn_buscar = st.form_submit_button("Buscar")

        if btn_buscar:
            if not id_busca.strip():
                st.error("Informe o ID do programa.")
            else:
                f = fidelidade_dao.buscar_por_id(id_busca.strip())
                if not f:
                    st.warning("Programa de fidelidade não encontrado.")
                else:
                    with st.form(key="form_atualizar_fidelidade", clear_on_submit=False):
                        st.markdown(f"**ID:** {f.id}")
                        st.markdown(f"**Cliente Atual:** {f.cliente_nome} (ID: {f.cliente_id})")
                        novos_pontos = st.number_input("Pontos*", min_value=0, step=1, value=f.pontos)
                        novo_nivel = st.selectbox(
                            "Nível*",
                            ["bronze", "prata", "ouro"],
                            index=["bronze", "prata", "ouro"].index(f.nivel.lower())
                        )
                        nova_validade = st.date_input(
                            "Data de Validade*",
                            value=datetime.strptime(f.validade, "%Y-%m-%d").date(),
                            min_value=date.today()
                        )
                        btn_atualizar = st.form_submit_button("Salvar Atualização")

                    if btn_atualizar:
                        f.pontos = int(novos_pontos)
                        f.nivel = novo_nivel
                        f.validade = nova_validade.strftime("%Y-%m-%d")
                        f.data_atualizacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ok, msg = fidelidade_dao.atualizar(f)
                        if ok:
                            st.success("Programa de fidelidade atualizado com sucesso!")
                        else:
                            st.error(f"Erro ao atualizar fidelidade: {msg}")

        return

    # ======================
    # 4. Deletar
    # ======================
    if escolha == "Deletar":
        st.subheader("❌ Deletar Programa de Fidelidade")
        with st.form(key="form_deletar_fidelidade"):
            id_del = st.text_input("ID do Programa para deletar*", max_chars=50)
            btn_deletar = st.form_submit_button("Deletar")

        if btn_deletar:
            if not id_del.strip():
                st.error("Informe o ID do programa.")
            else:
                f = fidelidade_dao.buscar_por_id(id_del.strip())
                if not f:
                    st.warning("Programa de fidelidade não encontrado.")
                else:
                    ok, msg = fidelidade_dao.deletar(id_del.strip())
                    if ok:
                        st.success("Programa de fidelidade deletado com sucesso!")
                    else:
                        st.error(f"Erro ao deletar fidelidade: {msg}")

        return

    st.error("Ação inválida.")
