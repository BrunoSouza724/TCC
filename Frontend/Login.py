import streamlit as st
import app

# Simulação de um "banco" de usuários
user_db = {"admin": "1234"}

def verificar_login(username, password):
    return user_db.get(username) == password

def criar_usuario(username, password):
    if username in user_db:
        return False
    user_db[username] = password
    return True

# Inicializa o estado se não existir
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

if st.session_state.logged_in:
    st.write(f"Bem-vindo, {st.session_state.username}!")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.stop() 
    else:
        # Exibe o app principal
        app.main()
    st.stop()  
else:
    st.title("Tela de Login")

    menu = st.radio("Escolha uma opção:", ["Login", "Criar Conta"])

    if menu == "Login":
        st.subheader("Acessar Conta")
        # Usando formulários:
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
                        st.stop()
                    else:
                        st.error("Usuário ou senha incorretos.")
                else:
                    st.warning("Por favor, preencha todos os campos.")

    elif menu == "Criar Conta":
        st.subheader("Criar Nova Conta")
        with st.form("create_form"):
            new_username = st.text_input("Novo Usuário", placeholder="Digite um nome de usuário")
            new_password = st.text_input("Nova Senha", type="password", placeholder="Digite uma senha")
            create_submitted = st.form_submit_button("Criar Conta")

            if create_submitted:
                if new_username and new_password:
                    if criar_usuario(new_username, new_password):
                        st.success(f"Conta criada com sucesso! Agora você pode fazer login como {new_username}.")
                    else:
                        st.error("Usuário já existe. Escolha outro nome.")
                else:
                    st.warning("Por favor, preencha todos os campos.")
