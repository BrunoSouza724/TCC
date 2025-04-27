import streamlit as st
import app 

# Entrada no site
user_db = {"admin": "1234"}  

# Função para verificar login
def verificar_login(username, password):
    """Função simplificada de verificação"""
    return user_db.get(username) == password

#Configuração do front
def aplicar_tema():
    st.markdown("""
    <style>
        :root {
            --primary: #FFFFFF;       /* Fundo branco da página */
            --secondary: #E8F5E9;     /* Verde MUITO claro (fundo do quadro) */
            --accent: #2E8B57;        /* Verde floresta (botões/bordas) */
            --text: #333333;          /* Texto escuro */
        }
        
        /* Quadro do login - AGORA COM FUNDO VERDE CLARO */
        [data-testid="stForm"] {
            background-color: var(--secondary) !important;  /* Verde claro */
            border: 2px solid var(--accent) !important;    /* Borda verde floresta */
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(46, 139, 87, 0.15);
        }
        
        /* Inputs - Estilo harmonizado */
        .stTextInput>div>div>input,
        .stPassword>div>div>input {
            background-color: white !important;
            border: 1px solid var(--accent) !important;
            border-radius: 6px;
        }
        
        /* Botões - Destaque */
        .stButton>button {
            background-color: var(--accent) !important;
            color: white !important;
            font-weight: bold;
            border-radius: 6px;
        }
        
        /* Título do formulário */
        h3 {
            color: var(--accent) !important;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    
def tela_login():
    col1, col2, col3 = st.columns([1,3,1])
    with col2:

        # Título centralizado
        st.markdown("<h1 style='text-align: center; color: #2E8B57;'>Login</h1>", 
                   unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Usuário", placeholder="Digite seu usuário")
            password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            
            if st.form_submit_button("Acessar Sistema"):
                if username and password:
                    if verificar_login(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Credenciais inválidas!")
                else:
                    st.warning("Preencha todos os campos!")

# Tela principal do aplicativo após login
def tela_principal():
    """Tela após login"""
    with st.sidebar:
        st.success(f"Bem-vindo, {st.session_state.username}!")
        if st.button("Sair"):
            st.session_state.clear()
            st.rerun()
    
    app.main() 
    
def main():
    aplicar_tema()
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if st.session_state.logged_in:
        tela_principal()
    else:
        tela_login()

if __name__ == "__main__":
    main()
