import streamlit as st
from dao.cliente_dao import ClienteDAO
from models.cliente import Cliente
from views.utils import buscar_por_campo_unico
from datetime import datetime

def cliente_page():
    st.title("🧑 Gestão de Clientes")
    cliente_dao = ClienteDAO()

    menu = ["Cadastrar", "Listar", "Atualizar", "Deletar"]
    escolha = st.sidebar.selectbox("Ações (Cliente)", menu)

    # ======================
    # 1. Cadastrar
    # ======================
    if escolha == "Cadastrar":
        st.subheader("➕ Cadastrar Novo Cliente")
        with st.form(key="form_cadastrar_cliente", clear_on_submit=True):
            nome = st.text_input("Nome Completo*", max_chars=100)
            cpf = st.text_input("CPF/CNPJ*", max_chars=18)
            email = st.text_input("E-mail", max_chars=100)
            telefone = st.text_input("Telefone", max_chars=15)
            endereco = st.text_input("Endereço Completo", max_chars=200)
            sms = st.checkbox("Opt-in SMS")
            email_opt = st.checkbox("Opt-in E-mail")
            whatsapp = st.checkbox("Opt-in WhatsApp")
            preferencias = st.text_input("Preferências (separe por vírgula)", max_chars=200)
            btn_salvar = st.form_submit_button("Salvar Cliente")

        if btn_salvar:
            erros = []
            if not nome.strip():
                erros.append("O campo Nome é obrigatório.")
            if not cpf.strip():
                erros.append("O campo CPF/CNPJ é obrigatório.")
            if erros:
                for e in erros:
                    st.error(e)
            else:
                cliente = Cliente(
                    id=None,
                    nome=nome.strip(),
                    cpf=cpf.strip(),
                    email=email.strip(),
                    telefone=telefone.strip(),
                    endereco=endereco.strip(),
                    preferencias=[p.strip() for p in preferencias.split(",")] if preferencias else [],
                    opt_in={"sms": sms, "email": email_opt, "whatsapp": whatsapp},
                    data_criacao=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                ok, msg = cliente_dao.criar(cliente)
                if ok:
                    st.success(f"Cliente '{nome}' cadastrado com sucesso!")
                else:
                    st.error(f"Erro ao cadastrar cliente: {msg}")

        return

    # ======================
    # 2. Listar
    # ======================
    if escolha == "Listar":
        st.subheader("📋 Lista de Clientes")
        clientes = cliente_dao.listar_todos()
        if not clientes:
            st.info("Nenhum cliente cadastrado.")
        else:
            dados = []
            for c in clientes:
                dados.append({
                    "ID": c.id,
                    "Nome": c.nome,
                    "CPF/CNPJ": c.cpf,
                    "E-mail": c.email or "",
                    "Telefone": c.telefone or "",
                    "Endereço": c.endereco or "",
                    "Opt-in SMS": "Sim" if c.opt_in.get("sms") else "Não",
                    "Opt-in E-mail": "Sim" if c.opt_in.get("email") else "Não",
                    "Opt-in WhatsApp": "Sim" if c.opt_in.get("whatsapp") else "Não",
                    "Preferências": ", ".join(c.preferencias) if c.preferencias else "",
                    "Data de Criação": c.data_criacao
                })
            st.table(dados)

        return

    # ======================
    # 3. Atualizar
    # ======================
    if escolha == "Atualizar":
        st.subheader("✏️ Atualizar Cliente")
        with st.form(key="form_buscar_cliente_atualizar"):
            cpf_busca = st.text_input("CPF/CNPJ para busca", max_chars=18)
            telefone_busca = st.text_input("Telefone para busca", max_chars=15)
            nome_busca = st.text_input("Nome para busca", max_chars=100)
            btn_buscar = st.form_submit_button("Buscar Cliente")

        if btn_buscar:
            cliente, erro = buscar_por_campo_unico(
                cliente_dao,
                cpf=cpf_busca.strip(),
                telefone=telefone_busca.strip(),
                nome=nome_busca.strip()
            )
            if not cliente:
                st.error(erro)
            else:
                with st.form(key="form_atualizar_cliente", clear_on_submit=False):
                    st.markdown(f"**ID:** {cliente.id}")
                    novo_nome = st.text_input("Nome Completo*", value=cliente.nome, max_chars=100)
                    novo_cpf = st.text_input("CPF/CNPJ*", value=cliente.cpf, max_chars=18)
                    novo_email = st.text_input("E-mail", value=cliente.email or "", max_chars=100)
                    novo_telefone = st.text_input("Telefone", value=cliente.telefone or "", max_chars=15)
                    novo_endereco = st.text_input("Endereço Completo", value=cliente.endereco or "", max_chars=200)
                    sms = st.checkbox("Opt-in SMS", value=cliente.opt_in.get("sms", False))
                    email_opt = st.checkbox("Opt-in E-mail", value=cliente.opt_in.get("email", False))
                    whatsapp = st.checkbox("Opt-in WhatsApp", value=cliente.opt_in.get("whatsapp", False))
                    novas_preferencias = st.text_input(
                        "Preferências (separe por vírgula)",
                        value=", ".join(cliente.preferencias) if cliente.preferencias else "",
                        max_chars=200
                    )
                    btn_atualizar = st.form_submit_button("Salvar Atualização")

                if btn_atualizar:
                    erros = []
                    if not novo_nome.strip():
                        erros.append("O campo Nome é obrigatório.")
                    if not novo_cpf.strip():
                        erros.append("O campo CPF/CNPJ é obrigatório.")
                    if erros:
                        for e in erros:
                            st.error(e)
                    else:
                        cliente.nome = novo_nome.strip()
                        cliente.cpf = novo_cpf.strip()
                        cliente.email = novo_email.strip()
                        cliente.telefone = novo_telefone.strip()
                        cliente.endereco = novo_endereco.strip()
                        cliente.opt_in = {"sms": sms, "email": email_opt, "whatsapp": whatsapp}
                        cliente.preferencias = [p.strip() for p in novas_preferencias.split(",")] if novas_preferencias else []
                        cliente.data_atualizacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        ok, msg = cliente_dao.atualizar(cliente)
                        if ok:
                            st.success("Cliente atualizado com sucesso!")
                        else:
                            st.error(f"Erro ao atualizar cliente: {msg}")

        return

    # ======================
    # 4. Deletar
    # ======================
    if escolha == "Deletar":
        st.subheader("❌ Deletar Cliente")
        with st.form(key="form_buscar_cliente_deletar"):
            cpf_busca = st.text_input("CPF/CNPJ para busca", max_chars=18)
            telefone_busca = st.text_input("Telefone para busca", max_chars=15)
            nome_busca = st.text_input("Nome para busca", max_chars=100)
            btn_buscar = st.form_submit_button("Buscar Cliente")

        if btn_buscar:
            cliente, erro = buscar_por_campo_unico(
                cliente_dao,
                cpf=cpf_busca.strip(),
                telefone=telefone_busca.strip(),
                nome=nome_busca.strip()
            )
            if not cliente:
                st.error(erro)
            else:
                st.warning(f"Tem certeza que deseja deletar o cliente: {cliente.nome} (ID: {cliente.id})?")
                if st.button("Confirmar Exclusão"):
                    ok, msg = cliente_dao.deletar(cliente.id)
                    if ok:
                        st.success("Cliente deletado com sucesso!")
                    else:
                        st.error(f"Erro ao deletar cliente: {msg}")

        return

    st.error("Ação inválida.")
