import streamlit as st
import app  

# Simula um banco de dados em memória (use um banco real em produção)
user_db = {"admin": "1234"}

# Função para verificar login
def verificar_login(username, password):
    return user_db.get(username) == password

# Função para criar um novo usuário
def criar_usuario(username, password):
    if username in user_db:
        return False  # Usuário já existe
    user_db[username] = password
    return True

# Inicializa o estado de sessão
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# Interface de login e criação de conta
def mostrar_login():
    st.title("Tela de Login")

    # Escolha entre login e criação de conta
    menu = st.radio("Escolha uma opção:", ["Login", "Criar Conta"])

    if menu == "Login":
        st.subheader("Acessar Conta")
        username = st.text_input("Usuário", placeholder="Digite seu usuário", key="login_user")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha", key="login_pass")

        if st.button("Login"):
            if username and password:
                if verificar_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                else:
                    st.error("Usuário ou senha incorretos.")
            else:
                st.warning("Por favor, preencha todos os campos.")

    elif menu == "Criar Conta":
        st.subheader("Criar Nova Conta")
        new_username = st.text_input("Novo Usuário", placeholder="Digite um nome de usuário", key="create_user")
        new_password = st.text_input("Nova Senha", type="password", placeholder="Digite uma senha", key="create_pass")

        if st.button("Criar Conta"):
            if new_username and new_password:
                if criar_usuario(new_username, new_password):
                    st.success(f"Conta criada com sucesso! Agora você pode fazer login como {new_username}.")
                else:
                    st.error("Usuário já existe. Escolha outro nome.")
            else:
                st.warning("Por favor, preencha todos os campos.")

# Função de logout
def logout():
    st.session_state.logged_in = False
    st.session_state.username = None

# Lógica principal
if st.session_state.logged_in:
    # Substitui a tela de login pelo app principal
    st.write(f"Bem-vindo, {st.session_state.username}!")
    if st.button("Logout"):
        logout()
        st.experimental_rerun() 
    else:
        # Chama a função principal do app importado
        app.main()  
else:
    mostrar_login()
