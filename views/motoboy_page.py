import streamlit as st
from dao.motoboy_dao import MotoboyDAO
from models.motoboy import Motoboy
from views.utils import buscar_por_campo_unico
from datetime import datetime

def motoboy_page():
    st.markdown("### 🛵 Gestão de Entregadores")
    motoboy_dao = MotoboyDAO()

    menu = ["Cadastrar", "Listar", "Atualizar", "Deletar"]
    escolha = st.sidebar.selectbox("Ações (Motoboy)", menu)

    # ======================
    # 1. Cadastrar
    # ======================
    if escolha == "Cadastrar":
        st.subheader("➕ Cadastrar novo Entregador")
        with st.form(key="form_cadastrar_motoboy", clear_on_submit=True):
            nome = st.text_input("Nome Completo*", max_chars=100)
            cpf = st.text_input("CPF*", max_chars=18)
            cnh = st.text_input("CNH*", max_chars=20)
            telefone = st.text_input("Telefone", max_chars=15)
            status = st.selectbox("Status Operacional*", ["Online", "Offline"])
            zonas = st.text_input("Zonas de Atuação (separe por vírgula)", max_chars=200)
            horarios = st.text_input("Horários Disponíveis (separe por vírgula)", max_chars=200)
            btn_salvar = st.form_submit_button("Salvar Entregador")

        if btn_salvar:
            erros = []
            if not nome.strip():
                erros.append("O campo Nome é obrigatório.")
            if not cpf.strip():
                erros.append("O campo CPF é obrigatório.")
            if not cnh.strip():
                erros.append("O campo CNH é obrigatório.")
            if erros:
                for e in erros:
                    st.error(e)
            else:
                motoboy = Motoboy(
                    id=None,
                    nome=nome.strip(),
                    cpf=cpf.strip(),
                    cnh=cnh.strip(),
                    telefone=telefone.strip(),
                    status_operacional=status,
                    zonas_atuacao=[z.strip() for z in zonas.split(",")] if zonas else [],
                    horarios_disponiveis=[h.strip() for h in horarios.split(",")] if horarios else [],
                    data_criacao=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                ok, msg = motoboy_dao.criar(motoboy)
                if ok:
                    st.success(f"Entregador '{nome}' cadastrado com sucesso!")
                else:
                    st.error(f"Erro ao cadastrar motoboy: {msg}")

        return

    # ======================
    # 2. Listar
    # ======================
    if escolha == "Listar":
        st.subheader("📋 Lista de Entregadores")
        motoboys = motoboy_dao.listar_todos()
        if not motoboys:
            st.info("Nenhum motoboy cadastrado.")
        else:
            dados = []
            for m in motoboys:
                dados.append({
                    "ID": m.id,
                    "Nome": m.nome,
                    "CPF": m.cpf,
                    "CNH": m.cnh,
                    "Telefone": m.telefone or "",
                    "Status": m.status_operacional,
                    "Zonas de Atuação": ", ".join(m.zonas_atuacao) if m.zonas_atuacao else "",
                    "Horários Disponíveis": ", ".join(m.horarios_disponiveis) if m.horarios_disponiveis else "",
                    "Data de Criação": m.data_criacao
                })
            st.table(dados)

        return

    # ======================
    # 3. Atualizar
    # ======================
    if escolha == "Atualizar":
        st.subheader("✏️ Atualizar Entregador")
        with st.form(key="form_buscar_motoboy"):
            cpf_busca = st.text_input("CPF para busca", max_chars=18)
            telefone_busca = st.text_input("Telefone para busca", max_chars=15)
            nome_busca = st.text_input("Nome para busca", max_chars=100)
            btn_buscar = st.form_submit_button("Buscar")

        if btn_buscar:
            m, erro = buscar_por_campo_unico(
                motoboy_dao,
                cpf=cpf_busca.strip(),
                telefone=telefone_busca.strip(),
                nome=nome_busca.strip()
            )
            if not m:
                st.error(erro)
            else:
                with st.form(key="form_atualizar_motoboy", clear_on_submit=False):
                    st.markdown(f"**ID:** {m.id}")
                    novo_nome = st.text_input("Nome Completo*", value=m.nome, max_chars=100)
                    novo_telefone = st.text_input("Telefone", value=m.telefone or "", max_chars=15)
                    novo_status = st.selectbox(
                        "Status Operacional*",
                        ["Online", "Offline"],
                        index=0 if m.status_operacional.lower() == "online" else 1
                    )
                    novas_zonas = st.text_input(
                        "Zonas de Atuação (separe por vírgula)",
                        value=", ".join(m.zonas_atuacao) if m.zonas_atuacao else "",
                        max_chars=200
                    )
                    novos_horarios = st.text_input(
                        "Horários Disponíveis (separe por vírgula)",
                        value=", ".join(m.horarios_disponiveis) if m.horarios_disponiveis else "",
                        max_chars=200
                    )
                    btn_atualizar = st.form_submit_button("Salvar Atualização")

                if btn_atualizar:
                    erros = []
                    if not novo_nome.strip():
                        erros.append("O campo Nome é obrigatório.")
                    if erros:
                        for e in erros:
                            st.error(e)
                    else:
                        m.nome = novo_nome.strip()
                        m.telefone = novo_telefone.strip()
                        m.status_operacional = novo_status
                        m.zonas_atuacao = [z.strip() for z in novas_zonas.split(",")] if novas_zonas else []
                        m.horarios_disponiveis = [h.strip() for h in novos_horarios.split(",")] if novos_horarios else []
                        m.data_atualizacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ok, msg = motoboy_dao.atualizar(m)
                        if ok:
                            st.success("Entregador atualizado com sucesso!")
                        else:
                            st.error(f"Erro ao atualizar motoboy: {msg}")

        return

    # ======================
    # 4. Deletar
    # ======================
    if escolha == "Deletar":
        st.subheader("❌ Deletar Entregador")
        with st.form(key="form_deletar_motoboy"):
            cpf_busca = st.text_input("CPF para busca", max_chars=18)
            telefone_busca = st.text_input("Telefone para busca", max_chars=15)
            nome_busca = st.text_input("Nome para busca", max_chars=100)
            btn_buscar = st.form_submit_button("Buscar")

        if btn_buscar:
            m, erro = buscar_por_campo_unico(
                motoboy_dao,
                cpf=cpf_busca.strip(),
                telefone=telefone_busca.strip(),
                nome=nome_busca.strip()
            )
            if not m:
                st.error(erro)
            else:
                st.warning(f"Tem certeza que deseja deletar o entregador: {m.nome} (ID: {m.id})?")
                if st.button("Confirmar Exclusão"):
                    ok, msg = motoboy_dao.deletar(m.id)
                    if ok:
                        st.success("Entregador deletado com sucesso!")
                    else:
                        st.error(f"Erro ao deletar entregador: {msg}")

        return

    st.error("Ação inválida.")
