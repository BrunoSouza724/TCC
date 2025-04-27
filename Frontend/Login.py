import streamlit as st
import app 

# Simulação de um "banco" de usuários
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
            --primary: #FFFFFF;       /* Fundo branco */
            --secondary: #F8F8F8;     /* Cinza muito claro */
            --accent: #2E8B57;        /* Verde floresta (principal) */
            --text: #333333;          /* Texto escuro */
            --border: #2E8B57;        /* Borda verde */
        }
        
        /* Quadro do login */
        [data-testid="stForm"] {
            background-color: var(--primary);
            border: 2px solid var(--border);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(46, 139, 87, 0.1); /* Sombra sutil verde */
        }
        
        /* Botões */
        .stButton>button {
            background-color: var(--accent) !important;
            color: white !important;
            border: none;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            opacity: 0.9;
            transform: scale(1.02);
        }
        
        /* Inputs */
        .stTextInput>div>div>input,
        .stPassword>div>div>input {
            background-color: var(--secondary) !important;
            border: 1px solid var(--border) !important;
        }
        
        /* Título do formulário */
        h3 {
            color: var(--accent) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
def tela_login():
    """Tela de login estilizada"""
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.image("Logo.png", width=200)  # Sua logo
        st.markdown("<h1 style='text-align: center;'>Controle Financeiro</h1>", unsafe_allow_html=True)
        
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
