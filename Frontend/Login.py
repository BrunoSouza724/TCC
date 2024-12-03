import streamlit as st
import subprocess
import os

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

# Interface principal
def mostrar_login():
    st.title("Tela de Login")

    # Escolha entre login e criação de conta
    menu = st.radio("Escolha uma opção:", ["Login", "Criar Conta"])

    if menu == "Login":
        st.subheader("Acessar Conta")
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
 
        if st.button("Login"):
            if username and password:
                if verificar_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username

                    # Caminho absoluto do arquivo app.py
                    app_path = os.path.abspath("app.py")

                    # Exibe mensagem e inicia o app principal
                    st.success(f"Login bem-sucedido! Bem-vindo(a), {username}!")
                    try: #O erro está aqui, verificar
                        subprocess.Popen(["streamlit", "run", app_path])
                        st.write("O aplicativo principal foi iniciado em uma nova aba.")
                        st.markdown(
                            """
                            <script>
                                window.close();
                            </script>
                            """,
                            unsafe_allow_html=True
                        ) #Erro
                    except Exception as e:
                        st.error(f"Erro ao abrir a tela principal: {e}")
                else:
                    st.error("Usuário ou senha incorretos.")
            else:
                st.warning("Por favor, preencha todos os campos.")

    elif menu == "Criar Conta":
        st.subheader("Criar Nova Conta")
        new_username = st.text_input("Novo Usuário", placeholder="Digite um nome de usuário")
        new_password = st.text_input("Nova Senha", type="password", placeholder="Digite uma senha")

        if st.button("Criar Conta"):
            if new_username and new_password:
                if criar_usuario(new_username, new_password):
                    st.success(f"Conta criada com sucesso! Agora você pode fazer login como {new_username}.")
                else:
                    st.error("Usuário já existe. Escolha outro nome.")
            else:
                st.warning("Por favor, preencha todos os campos.")

# Lógica de fluxo
if st.session_state.logged_in:
    # Substitui o conteúdo da página de login
    st.write("Você já está logado. O aplicativo principal foi aberto em outra aba.")
else:
    # Mostra a tela de login
    mostrar_login()
