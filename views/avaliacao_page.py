import streamlit as st
from models.avaliacao import Avaliacao
from dao.avaliacao_dao import AvaliacaoDAO
from datetime import datetime
from views.utils import buscar_por_campo_unico
from dao.cliente_dao import ClienteDAO
from dao.motoboy_dao import MotoboyDAO

def avaliacao_page(perfil, usuario, modo=None):
    st.title("Avaliações")
    avaliacao_dao = AvaliacaoDAO()

    # Funcionário/Admin: acesso total
    if perfil == "Funcionário":
        menu = ["Cadastrar", "Listar", "Dashboard", "Atualizar", "Deletar"]
        escolha = st.sidebar.selectbox("Ações", menu)

        if escolha == "Cadastrar":
            st.subheader("Cadastrar Avaliação")
            avaliador = st.text_input("Avaliador")
            avaliado = st.text_input("Avaliado")
            nota = st.slider("Nota", 1, 5)
            comentario = st.text_area("Comentário")
            if st.button("Salvar Avaliação"):
                avaliacao = Avaliacao(
                    id=None,
                    avaliador=avaliador,
                    avaliado=avaliado,
                    nota=nota,
                    comentario=comentario,
                    data_hora=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                avaliacao_dao.criar(avaliacao)
                st.success("Avaliação cadastrada com sucesso!")

        elif escolha == "Listar":
            st.subheader("Listar Avaliações")
            avaliacoes = avaliacao_dao.listar_todos()
            if not avaliacoes:
                st.info("Nenhuma avaliação cadastrada.")
            else:
                for a in avaliacoes:
                    st.markdown(f"**ID:** {a.id}")
                    st.markdown(f"**Avaliador:** {a.avaliador}")
                    st.markdown(f"**Avaliado:** {a.avaliado}")
                    st.markdown(f"**Nota:** {a.nota}")
                    st.markdown(f"**Comentário:** {a.comentario}")
                    st.markdown(f"**Data/Hora:** {a.data_hora}")
                    st.markdown("---")

        elif escolha == "Dashboard":
            st.subheader("Dashboard de Avaliações")
            avaliacoes = avaliacao_dao.listar_todos()
            if not avaliacoes:
                st.info("Nenhuma avaliação cadastrada.")
            else:
                notas = [a.nota for a in avaliacoes]
                st.write(f"Média das notas: {sum(notas)/len(notas):.2f}")
                st.bar_chart(notas)

        elif escolha == "Atualizar":
            st.subheader("Atualizar Avaliação")
            id_avaliacao = st.text_input("ID da Avaliação")
            if st.button("Buscar"):
                avaliacao = avaliacao_dao.buscar_por_id(id_avaliacao)
                if avaliacao:
                    nova_nota = st.slider("Nova Nota", 1, 5, value=avaliacao.nota)
                    novo_comentario = st.text_area("Novo Comentário", value=avaliacao.comentario)
                    if st.button("Salvar Atualização"):
                        avaliacao.nota = nova_nota
                        avaliacao.comentario = novo_comentario
                        avaliacao.data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        avaliacao_dao.atualizar(avaliacao)
                        st.success("Avaliação atualizada com sucesso!")
                else:
                    st.warning("Avaliação não encontrada.")

        elif escolha == "Deletar":
            st.subheader("Deletar Avaliação")
            id_avaliacao = st.text_input("ID da Avaliação para deletar")
            if st.button("Deletar"):
                if avaliacao_dao.deletar(id_avaliacao):
                    st.success("Avaliação deletada com sucesso!")
                else:
                    st.warning("Avaliação não encontrada.")
                    
    if perfil == "Motoboy" and modo == "avaliar_cliente":
        st.subheader("Avaliar Cliente")
        cpf = st.text_input("CPF do Cliente")
        telefone = st.text_input("Telefone do Cliente")
        nome_busca = st.text_input("Nome do Cliente")
        if st.button("Buscar Cliente"):
            cliente_dao = ClienteDAO()
            cliente, erro = buscar_por_campo_unico(cliente_dao, cpf=cpf, telefone=telefone, nome=nome_busca)
            if cliente:
                nota = st.slider("Nota", 1, 5)
                comentario = st.text_area("Comentário")
                if st.button("Salvar Avaliação"):
                    avaliacao = Avaliacao(
                        id=None,
                        avaliador=usuario,
                        avaliado=cliente.nome,
                        nota=nota,
                        comentario=comentario,
                        data_hora=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    avaliacao_dao.criar(avaliacao)
                    st.success("Avaliação cadastrada com sucesso!")
            else:
                st.error(erro)

        elif modo == "minhas_avaliacoes":
            st.subheader("Minhas Avaliações Realizadas")
            avaliacoes = avaliacao_dao.listar_por_avaliador(usuario)
            if not avaliacoes:
                st.info("Você ainda não fez avaliações.")
            else:
                for a in avaliacoes:
                    st.markdown(f"**ID:** {a.id}")
                    st.markdown(f"**Cliente Avaliado:** {a.avaliado}")
                    st.markdown(f"**Nota:** {a.nota}")
                    st.markdown(f"**Comentário:** {a.comentario}")
                    st.markdown(f"**Data/Hora:** {a.data_hora}")
                    st.markdown("---")

    elif perfil == "Cliente" and modo == "avaliar_motoboy":
        st.subheader("Avaliar Motoboy")
        cpf = st.text_input("CPF do Motoboy")
        telefone = st.text_input("Telefone do Motoboy")
        nome_busca = st.text_input("Nome do Motoboy")
        if st.button("Buscar Motoboy"):
            motoboy_dao = MotoboyDAO()
            motoboy, erro = buscar_por_campo_unico(motoboy_dao, cpf=cpf, telefone=telefone, nome=nome_busca)
            if motoboy:
                nota = st.slider("Nota", 1, 5)
                comentario = st.text_area("Comentário")
                if st.button("Salvar Avaliação"):
                    avaliacao = Avaliacao(
                        id=None,
                        avaliador=usuario,
                        avaliado=motoboy.nome,
                        nota=nota,
                        comentario=comentario,
                        data_hora=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    avaliacao_dao.criar(avaliacao)
                    st.success("Avaliação cadastrada com sucesso!")
            else:
                st.error(erro)