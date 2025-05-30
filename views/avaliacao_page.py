import streamlit as st
from models.avaliacao import Avaliacao
from dao.avaliacao_dao import AvaliacaoDAO
from datetime import datetime


def avaliacao_page():
    st.title("Gestão de Avaliações 360°")

    avaliacao_dao = AvaliacaoDAO()

    menu = ["Cadastrar", "Listar", "Dashboard", "Atualizar", "Deletar"]
    escolha = st.sidebar.selectbox("Menu Avaliação", menu)

    if escolha == "Cadastrar":
        st.subheader("Cadastrar Nova Avaliação")

        avaliador = st.selectbox("Quem está avaliando?", ["cliente", "motoboy", "pizzaria"])
        avaliado = st.text_input("Avaliando quem ou o quê? (Ex.: 'motoboy:123', 'produto:calabresa')")
        nota = st.slider("Nota", 1, 5)
        comentario = st.text_area("Comentário")

        if st.button("Salvar"):
            avaliacao = Avaliacao(
                id=None,
                avaliador=avaliador,
                avaliado=avaliado,
                nota=nota,
                comentario=comentario
            )
            avaliacao_dao.criar(avaliacao)
            st.success("Avaliação cadastrada com sucesso!")

    elif escolha == "Listar":
        st.subheader("Lista de Avaliações")
        avaliacoes = avaliacao_dao.listar_todos()

        for a in avaliacoes:
            st.markdown(f"**ID:** {a.id}")
            st.markdown(f"**Avaliador:** {a.avaliador}")
            st.markdown(f"**Avaliado:** {a.avaliado}")
            st.markdown(f"**Nota:** {a.nota}")
            st.markdown(f"**Comentário:** {a.comentario}")
            st.markdown(f"**Data/Hora:** {a.data_hora}")
            st.markdown("---")

    elif escolha == "Dashboard":
        st.subheader("Dashboard de Feedback")

        avaliacoes = avaliacao_dao.listar_todos()

        if not avaliacoes:
            st.warning("Nenhuma avaliação cadastrada.")
            return

        filtro_avaliador = st.multiselect(
            "Filtrar por Avaliador",
            options=list(set([a.avaliador for a in avaliacoes])),
            default=list(set([a.avaliador for a in avaliacoes]))
        )

        filtro_avaliado = st.text_input("Filtrar por Avaliado (Deixe vazio para todos)")

        filtradas = [
            a for a in avaliacoes
            if a.avaliador in filtro_avaliador and (filtro_avaliado.lower() in a.avaliado.lower() if filtro_avaliado else True)
        ]

        if filtradas:
            notas = [a.nota for a in filtradas]
            media = sum(notas) / len(notas)

            st.metric("Quantidade de Avaliações", len(filtradas))
            st.metric("Média das Notas", f"{media:.2f}")

            st.bar_chart(
                data={str(n): notas.count(n) for n in range(1, 6)},
                use_container_width=True
            )

            with st.expander("Ver detalhes das avaliações"):
                for a in filtradas:
                    st.markdown(f"**Avaliador:** {a.avaliador}")
                    st.markdown(f"**Avaliado:** {a.avaliado}")
                    st.markdown(f"**Nota:** {a.nota}")
                    st.markdown(f"**Comentário:** {a.comentario}")
                    st.markdown(f"**Data/Hora:** {a.data_hora}")
                    st.markdown("---")
        else:
            st.info("Nenhuma avaliação encontrada com os filtros selecionados.")

    elif escolha == "Atualizar":
        st.subheader("Atualizar Avaliação")
        id_avaliacao = st.text_input("ID da Avaliação")

        if st.button("Buscar"):
            a = avaliacao_dao.buscar_por_id(id_avaliacao)
            if a:
                nota = st.slider("Nota", 1, 5, a.nota)
                comentario = st.text_area("Comentário", a.comentario)

                if st.button("Atualizar"):
                    a.nota = nota
                    a.comentario = comentario
                    a.data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    avaliacao_dao.atualizar(a)
                    st.success("Avaliação atualizada com sucesso!")
            else:
                st.error("Avaliação não encontrada.")

    elif escolha == "Deletar":
        st.subheader("Deletar Avaliação")
        id_avaliacao = st.text_input("ID da Avaliação")

        if st.button("Deletar"):
            a = avaliacao_dao.buscar_por_id(id_avaliacao)
            if a:
                avaliacao_dao.deletar(id_avaliacao)
                st.success("Avaliação deletada com sucesso!")
            else:
                st.error("Avaliação não encontrada.")