import streamlit as st
import app

# Simulação de um "banco" de usuários
user_db = {"admin": "1234"}

# Função para verificar login
def verificar_login(username, password):
    return user_db.get(username) == password

# Tela principal do aplicativo após login
def tela_principal():
    st.write(f"Bem-vindo, {st.session_state.username}!")
    if st.button("Logout"):
        # Limpa o estado de sessão ao fazer logout
        st.session_state.logged_in = False
        st.session_state.username = None
    else:
        # Chama o app principal
        app.main()

# Tela de login
def tela_login():
    st.title("Tela de Login")
    st.subheader("Acessar Conta")
    with st.form("login_form"):
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username and password:
                if verificar_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Bem-vindo, {st.session_state.username}!")
                    return  # Força o ciclo a sair da tela de login
                else:
                    st.error("Usuário ou senha incorretos.")
            else:
                st.warning("Por favor, preencha todos os campos.")

# Inicializa o estado do Streamlit
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# Controle principal
if st.session_state.logged_in:
    tela_principal()
else:
    tela_login()
