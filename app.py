import streamlit as st

from views.cliente_page import cliente_page
from views.motoboy_page import motoboy_page
from views.avaliacao_page import avaliacao_page
from views.dashboard_page import dashboard_page
from views.fidelidade_page import fidelidade_page
from views.campanha_page import campanha_page

# ----------------------------------------
# 1. Configuração inicial da página
# ----------------------------------------
def configurar_pagina():
    st.set_page_config(
        page_title="Sistema de Gestão - Pizzaria",
        page_icon="🍕"
    )

# ----------------------------------------
# 2. Inicialização do estado de sessão
# ----------------------------------------
def inicializar_estado():
    """
    Garante que as chaves de session_state existam antes de usar.
    """
    if "logado" not in st.session_state:
        st.session_state["logado"] = False
    if "usuario_nome" not in st.session_state:
        st.session_state["usuario_nome"] = ""
    if "usuario_perfil" not in st.session_state:
        st.session_state["usuario_perfil"] = ""

# ----------------------------------------
# 3. Tela de login (sem autenticação real)
# ----------------------------------------
def tela_login():
    """
    Exibe um formulário de login simples. Ao clicar em 'Entrar', define
    st.session_state["logado"], ["usuario_nome"] e ["usuario_perfil"], e
    chama st.rerun() para atualizar a interface.
    """
    st.title("🔒 Login")
    st.write("Use um dos seguintes pares para testar:")
    st.markdown(
        """
        - **Funcionário**: usuário `admin` / senha `admin`  
        - **Motoboy**: usuário `motoboy` / senha `123`  
        - **Cliente**: usuário `cliente` / senha `abc`
        """
    )

    with st.form(key="form_login", clear_on_submit=True):
        usuario = st.text_input("Usuário", max_chars=50)
        senha = st.text_input("Senha", type="password", max_chars=50)
        btn_entrar = st.form_submit_button("Entrar")

    if btn_entrar:
        usuario = usuario.strip()
        senha = senha.strip()

        # Simulação de autenticação
        if usuario == "admin" and senha == "admin":
            st.session_state["logado"] = True
            st.session_state["usuario_nome"] = "Administrador"
            st.session_state["usuario_perfil"] = "Funcionário"
        elif usuario == "motoboy" and senha == "123":
            st.session_state["logado"] = True
            st.session_state["usuario_nome"] = "Motoboy XPTO"
            st.session_state["usuario_perfil"] = "Motoboy"
        elif usuario == "cliente" and senha == "abc":
            st.session_state["logado"] = True
            st.session_state["usuario_nome"] = "Cliente XPTO"
            st.session_state["usuario_perfil"] = "Cliente"
        else:
            st.error("Usuário ou senha inválidos.")
            return

        # Se o login foi bem-sucedido, recarrega a página
        st.rerun()

# ----------------------------------------
# 4. Menu principal (após login)
# ----------------------------------------
def exibir_menu():
    """
    Exibe, na sidebar, a imagem e o menu conforme o perfil do usuário.
    Em seguida, chama a página correspondente à opção escolhida.
    """
    perfil = st.session_state["usuario_perfil"]
    nome = st.session_state["usuario_nome"]

    st.sidebar.image(
        "https://img.freepik.com/free-vector/pizza-logo-design_23-2149423871.jpg",
        width=150
    )
    st.sidebar.title(f"🍕 Bem-vindo, {nome} ({perfil})")
    st.sidebar.markdown("---")

    # Definição do menu conforme perfil
    if perfil == "Funcionário":
        opcoes = [
            "Dashboard Geral",
            "Clientes",
            "Motoboys",
            "Avaliações 360°",
            "Fidelidade",
            "Campanhas",
            "Sair"
        ]
    elif perfil == "Motoboy":
        opcoes = [
            "Avaliar Cliente",
            "Minhas Avaliações",
            "Sair"
        ]
    elif perfil == "Cliente":
        opcoes = [
            "Avaliar Pizzaria",
            "Avaliar Motoboy",
            "Sair"
        ]
    else:
        # Se o perfil for inválido ou vazio, força logout
        st.error("Perfil de usuário inválido. Faça login novamente.")
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.rerun()
        return

    escolha = st.sidebar.selectbox("Menu Principal", opcoes)

    # Ramo comum para botão “Sair”
    if escolha == "Sair":
        st.session_state.clear()
        st.rerun()
        return

    # Roteamento para cada opção de menu
    if perfil == "Funcionário":
        if escolha == "Dashboard Geral":
            dashboard_page()
        elif escolha == "Clientes":
            cliente_page()
        elif escolha == "Motoboys":
            motoboy_page()
        elif escolha == "Avaliações 360°":
            avaliacao_page(perfil=perfil, usuario=nome, modo="admin")
        elif escolha == "Fidelidade":
            fidelidade_page()
        elif escolha == "Campanhas":
            campanha_page()

    elif perfil == "Motoboy":
        if escolha == "Avaliar Cliente":
            avaliacao_page(perfil=perfil, usuario=nome, modo="avaliar_cliente")
        elif escolha == "Minhas Avaliações":
            avaliacao_page(perfil=perfil, usuario=nome, modo="minhas_avaliacoes")

    elif perfil == "Cliente":
        if escolha == "Avaliar Pizzaria":
            avaliacao_page(perfil=perfil, usuario=nome, modo="avaliar_pizzaria")
        elif escolha == "Avaliar Motoboy":
            avaliacao_page(perfil=perfil, usuario=nome, modo="avaliar_motoboy")

# ----------------------------------------
# 5. Função principal
# ----------------------------------------
def main():
    configurar_pagina()
    inicializar_estado()

    if not st.session_state["logado"]:
        tela_login()
    else:
        exibir_menu()

if __name__ == "__main__":
    main()
