import streamlit as st
from models.avaliacao import Avaliacao
from dao.avaliacao_dao import AvaliacaoDAO
from datetime import datetime
from views.utils import buscar_por_campo_unico
from dao.cliente_dao import ClienteDAO
from dao.motoboy_dao import MotoboyDAO

def avaliacao_page(perfil: str, usuario: str, modo: str = None):
    """
    Página de Avaliações, com diferentes comportamentos dependendo de:
      - perfil == "Funcionário": CRUD completo + Dashboard
      - perfil == "Motoboy" e modo == "avaliar_cliente": formulário de avaliação de cliente
      - perfil == "Motoboy" e modo == "minhas_avaliacoes": lista avaliações feitas pelo motoboy
      - perfil == "Cliente" e modo == "avaliar_motoboy": formulário de avaliação de motoboy
    """
    st.markdown("### ⭐ Avaliações")
    avaliacao_dao = AvaliacaoDAO()
    cliente_dao = ClienteDAO()
    motoboy_dao = MotoboyDAO()

    # ----------------------------
    # 1. PERFIL: Funcionário/Admin
    # ----------------------------
    if perfil == "Funcionário":
        menu = ["Cadastrar", "Listar", "Dashboard", "Atualizar", "Deletar"]
        escolha = st.sidebar.selectbox("Ações (Funcionário)", menu)

        # ===== 1.1 Cadastrar =====
        if escolha == "Cadastrar":
            st.subheader("➕ Cadastrar Nova Avaliação")
            with st.form(key="form_cadastrar_avaliacao", clear_on_submit=True):
                # Selecionar Avaliador (cliente ou motoboy) — você pode adaptar para lista fixa
                avaliador = st.text_input("Nome do Avaliador*", max_chars=100)
                avaliado = st.text_input("Nome do Avaliado*", max_chars=100)
                nota = st.slider("Nota (1 a 5)*", min_value=1, max_value=5, step=1)
                comentario = st.text_area("Comentário (opcional)")
                btn_salvar = st.form_submit_button("Salvar Avaliação")

            if btn_salvar:
                # Validações simples
                erros = []
                if not avaliador.strip():
                    erros.append("O campo Avaliador é obrigatório.")
                if not avaliado.strip():
                    erros.append("O campo Avaliado é obrigatório.")
                if erros:
                    for e in erros:
                        st.error(e)
                else:
                    nova = Avaliacao(
                        id=None,
                        avaliador=avaliador.strip(),
                        avaliado=avaliado.strip(),
                        nota=nota,
                        comentario=comentario.strip(),
                        data_hora=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    ok, msg = avaliacao_dao.criar(nova)
                    if ok:
                        st.success("Avaliação cadastrada com sucesso!")
                    else:
                        st.error(f"Erro ao salvar: {msg}")

        # ===== 1.2 Listar =====
        elif escolha == "Listar":
            st.subheader("📋 Todas as Avaliações")
            avaliacoes = avaliacao_dao.listar_todos()
            if not avaliacoes:
                st.info("Nenhuma avaliação cadastrada.")
            else:
                # Montar lista de dicionários para DataFrame ou st.table
                dados = []
                for a in avaliacoes:
                    dados.append({
                        "ID": a.id,
                        "Avaliador": a.avaliador,
                        "Avaliado": a.avaliado,
                        "Nota": a.nota,
                        "Comentário": a.comentario or "",
                        "Data/Hora": a.data_hora
                    })
                st.table(dados)

        # ===== 1.3 Dashboard =====
        elif escolha == "Dashboard":
            st.subheader("📊 Dashboard de Avaliações")
            avaliacoes = avaliacao_dao.listar_todos()
            if not avaliacoes:
                st.info("Nenhuma avaliação cadastrada.")
            else:
                notas = [a.nota for a in avaliacoes]
                media = sum(notas) / len(notas)
                st.metric("Média das notas", f"{media:.2f}")
                st.bar_chart(notas)

        # ===== 1.4 Atualizar =====
        elif escolha == "Atualizar":
            st.subheader("✏️ Atualizar Avaliação")
            with st.form(key="form_buscar_avaliacao_atualizar"):
                id_busca = st.text_input("ID da Avaliação para buscar*", max_chars=50)
                btn_buscar = st.form_submit_button("Buscar")

            if btn_buscar:
                if not id_busca.strip():
                    st.error("Informe o ID da avaliação.")
                else:
                    avaliacao = avaliacao_dao.buscar_por_id(id_busca.strip())
                    if not avaliacao:
                        st.warning("Avaliação não encontrada.")
                    else:
                        # Exibe formulário de atualização já preenchido
                        with st.form(key="form_atualizar_avaliacao", clear_on_submit=False):
                            st.markdown(f"**ID:** {avaliacao.id}")
                            st.markdown(f"**Avaliador Atual:** {avaliacao.avaliador}")
                            st.markdown(f"**Avaliado Atual:** {avaliacao.avaliado}")
                            nova_nota = st.slider(
                                "Nova Nota (1 a 5)*",
                                min_value=1, max_value=5, step=1,
                                value=avaliacao.nota
                            )
                            novo_comentario = st.text_area(
                                "Novo Comentário (opcional)",
                                value=avaliacao.comentario or ""
                            )
                            btn_salvar_update = st.form_submit_button("Salvar Atualização")

                        if btn_salvar_update:
                            avaliacao.nota = nova_nota
                            avaliacao.comentario = novo_comentario.strip()
                            avaliacao.data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            ok, msg = avaliacao_dao.atualizar(avaliacao)
                            if ok:
                                st.success("Avaliação atualizada com sucesso!")
                            else:
                                st.error(f"Erro ao atualizar: {msg}")

        # ===== 1.5 Deletar =====
        elif escolha == "Deletar":
            st.subheader("❌ Deletar Avaliação")
            with st.form(key="form_deletar_avaliacao"):
                id_del = st.text_input("ID da Avaliação para deletar*", max_chars=50)
                btn_deletar = st.form_submit_button("Deletar")

            if btn_deletar:
                if not id_del.strip():
                    st.error("Informe o ID da avaliação.")
                else:
                    ok, msg = avaliacao_dao.deletar(id_del.strip()), ""
                    if ok:
                        st.success("Avaliação deletada com sucesso!")
                    else:
                        st.warning("Avaliação não encontrada ou falha ao deletar.")

        return  # função encerra para perfil Funcionário

    # -------------------------------------------------
    # 2. PERFIL: Motoboy
    #    2.1 modo = "avaliar_cliente"
    #    2.2 modo = "minhas_avaliacoes"
    # -------------------------------------------------
    if perfil == "Motoboy":
        # 2.1 Avaliar Cliente
        if modo == "avaliar_cliente":
            st.subheader("➕ Avaliar Cliente")
            with st.form(key="form_buscar_cliente"):
                cpf = st.text_input("CPF do Cliente", max_chars=18)
                telefone = st.text_input("Telefone do Cliente", max_chars=15)
                nome_busca = st.text_input("Nome do Cliente", max_chars=100)
                btn_buscar = st.form_submit_button("Buscar Cliente")

            if btn_buscar:
                cliente, erro = buscar_por_campo_unico(
                    cliente_dao, cpf=cpf.strip(), telefone=telefone.strip(), nome=nome_busca.strip()
                )
                if not cliente:
                    st.error(erro)
                else:
                    # Cliente encontrado, exibir formulário de avaliação
                    with st.form(key="form_avaliar_cliente", clear_on_submit=True):
                        st.markdown(f"Cliente selecionado: **{cliente.nome}**")
                        nota = st.slider("Nota para o Cliente (1 a 5)*", min_value=1, max_value=5, step=1)
                        comentario = st.text_area("Comentário (opcional)")
                        btn_salvar = st.form_submit_button("Salvar Avaliação")

                    if btn_salvar:
                        avaliacao = Avaliacao(
                            id=None,
                            avaliador=usuario,
                            avaliado=cliente.nome,
                            nota=nota,
                            comentario=comentario.strip(),
                            data_hora=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        )
                        ok, msg = avaliacao_dao.criar(avaliacao)
                        if ok:
                            st.success("Avaliação do cliente cadastrada com sucesso!")
                        else:
                            st.error(f"Erro ao salvar: {msg}")

            return  # encerra modo avaliar_cliente

        # 2.2 Minhas Avaliações
        if modo == "minhas_avaliacoes":
            st.subheader("🗒️ Minhas Avaliações de Cliente")
            avals = avaliacao_dao.listar_por_avaliador(usuario)
            if not avals:
                st.info("Você ainda não fez nenhuma avaliação.")
            else:
                dados = []
                for a in avals:
                    dados.append({
                        "ID": a.id,
                        "Cliente Avaliado": a.avaliado,
                        "Nota": a.nota,
                        "Comentário": a.comentario or "",
                        "Data/Hora": a.data_hora
                    })
                st.table(dados)
            return

    # -------------------------------------------------
    # 3. PERFIL: Cliente
    #    3.1 modo = "avaliar_motoboy"
    # -------------------------------------------------
    if perfil == "Cliente" and modo == "avaliar_motoboy":
        st.subheader("➕ Avaliar Motoboy")
        with st.form(key="form_buscar_motoboy"):
            cpf = st.text_input("CPF do Motoboy", max_chars=18)
            telefone = st.text_input("Telefone do Motoboy", max_chars=15)
            nome_busca = st.text_input("Nome do Motoboy", max_chars=100)
            btn_buscar = st.form_submit_button("Buscar Motoboy")

        if btn_buscar:
            motoboy, erro = buscar_por_campo_unico(
                motoboy_dao, cpf=cpf.strip(), telefone=telefone.strip(), nome=nome_busca.strip()
            )
            if not motoboy:
                st.error(erro)
            else:
                with st.form(key="form_avaliar_motoboy", clear_on_submit=True):
                    st.markdown(f"Motoboy selecionado: **{motoboy.nome}**")
                    nota = st.slider("Nota para o Motoboy (1 a 5)*", min_value=1, max_value=5, step=1)
                    comentario = st.text_area("Comentário (opcional)")
                    btn_salvar = st.form_submit_button("Salvar Avaliação")

                if btn_salvar:
                    avaliacao = Avaliacao(
                        id=None,
                        avaliador=usuario,
                        avaliado=motoboy.nome,
                        nota=nota,
                        comentario=comentario.strip(),
                        data_hora=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    ok, msg = avaliacao_dao.criar(avaliacao)
                    if ok:
                        st.success("Avaliação do motoboy cadastrada com sucesso!")
                    else:
                        st.error(f"Erro ao salvar: {msg}")
        return

    # ----------------------------
    # 4. Caso nenhum perfil/modo
    # ----------------------------
    st.error("Acesso negado ou modo inválido.")