import streamlit as st
import sqlite3

# Conexão com o banco de dados
def conectar_banco():
    return sqlite3.connect('Lancamentos.db')

def Teste_Entrada():
    st.title(':credit_card: Entrada e Saída')

    # Inicializar session_state
    if "formulario_visivel" not in st.session_state:
        st.session_state.formulario_visivel = True
    if "salvo" not in st.session_state:
        st.session_state.salvo = False
    if "dados_transacao" not in st.session_state:
        st.session_state.dados_transacao = {}
    if "tela_atual" not in st.session_state:
        st.session_state.tela_atual = "entrada_saida"

    # Função para salvar no banco de dados
    def salvar_transacao():
        dados = st.session_state.dados_transacao
        if not dados.get("descricao"):
            st.error("Selecione ao menos uma descrição.")
            return
        if dados.get("valor", 0) <= 0:
            st.error("O valor deve ser positivo.")
            return
        
        try:
            con = conectar_banco()
            cursor = con.cursor()
            cursor.execute(
                '''INSERT INTO Lancamentos (Tipo, Data, Descricao, Valor, Metodo)
                VALUES (?, ?, ?, ?, ?)''',
                (
                    dados["tipo"],
                    str(dados["data"]),
                    ', '.join(dados["descricao"]),
                    dados["valor"],
                    dados["metodo"],
                )
            )
            con.commit()
            st.success("Transação salva com sucesso!")
        except sqlite3.Error as e:
            st.error(f"Erro ao salvar: {e}")
        finally:
            con.close()
        
        st.session_state.formulario_visivel = False
        st.session_state.salvo = True

    def nova_transacao():
        st.session_state.formulario_visivel = True
        st.session_state.salvo = False
        st.session_state.dados_transacao = {}

    def voltar_menu():
        st.session_state.tela_atual = "menu"

    # Barra lateral
    st.sidebar.image('Logo.png')
    st.sidebar.title('Seja-Bem Vindo ao Controle Financeiro :heavy_dollar_sign:')

    # Formulário principal
    if st.session_state.tela_atual == "entrada_saida":
        if st.session_state.formulario_visivel:
            st.session_state.dados_transacao["tipo"] = st.radio(
                "Tipo de transação:", ["Entrada", "Saída"], horizontal=True, key="tipo"
            )
            st.session_state.dados_transacao["data"] = st.date_input(
                "Data da transação:", key="data"
            )
            st.session_state.dados_transacao["descricao"] = st.multiselect(
                "Descrição:", ["Caneta", "Lápis", "Caderno"], key="descricao"
            )
            st.session_state.dados_transacao["valor"] = st.number_input(
                "Valor (R$):", min_value=0.0, step=0.01, format="%.2f", key="valor"
            )
            st.session_state.dados_transacao["metodo"] = st.selectbox(
                "Método de pagamento:", ["Dinheiro", "Cartão de Crédito", "Cartão de Débito"], key="metodo"
            )

            st.button("Salvar", on_click=salvar_transacao)

        # Exibição após salvar
        if st.session_state.salvo and not st.session_state.formulario_visivel:
            dados = st.session_state.dados_transacao
            st.write("### Resumo da Transação")
            st.write(f"**Tipo:** {dados['tipo']}")
            st.write(f"**Data:** {dados['data']}")
            st.write(f"**Descrição:** {', '.join(dados['descricao'])}")
            st.write(f"**Valor:** R$ {dados['valor']:.2f}")
            st.write(f"**Método:** {dados['metodo']}")

            st.button("Nova Transação", on_click=nova_transacao)
            
