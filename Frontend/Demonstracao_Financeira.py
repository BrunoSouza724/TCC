import streamlit as st
import pandas as pd
import datetime
from sqlalchemy import create_engine

# -------------------------------------
# Configuração da Conexão com o Banco
# Ajuste de acordo com seu SGBD e credenciais
# Exemplo para MySQL:
# engine = create_engine("mysql+pymysql://usuario:senha@host:porta/banco")
# -------------------------------------
engine = None  # Remover essa linha e substituir pela sua engine real

# Título do aplicativo
st.title("Dashboard - Demonstrações Financeiras")

# -------------------------------------
# Seção Superior com 3 colunas
# -------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    data_selecionada = st.date_input("Data", datetime.date.today())

with col2:
    opcoes_dados = ["coluna1", "coluna2", "coluna3"]
    dado_selecionado = st.selectbox("Selecione o dado desejado", opcoes_dados)

with col3:
    # Incluímos "Ambas" como uma terceira opção
    tipo_transacao = st.radio("Entrada, Saída ou Ambas", ("Entrada", "Saída", "Ambas"))

# -------------------------------------
# Botão de busca
# -------------------------------------
if st.button("Buscar Dados"):
    # Monta a query de acordo com a opção de transação escolhida
    if tipo_transacao == "Ambas":
        # Não filtra por transação
        query = f"""
            SELECT *
            FROM sua_tabela
            WHERE DATE(data) = '{data_selecionada}'
              AND {dado_selecionado} IS NOT NULL
        """
    else:
        # Filtra pelo tipo de transação escolhido
        query = f"""
            SELECT *
            FROM sua_tabela
            WHERE DATE(data) = '{data_selecionada}'
              AND {dado_selecionado} IS NOT NULL
              AND transacao = '{tipo_transacao}'
        """

    # Executa a consulta
    if engine is not None:
        try:
            df = pd.read_sql(query, engine)
        except Exception as e:
            st.error(f"Erro ao consultar o banco de dados: {e}")
            df = pd.DataFrame()
    else:
        st.warning("Engine de conexão não configurada. Substitua 'engine' pela sua conexão real.")
        df = pd.DataFrame()

    # -------------------------------------
    # Seção Inferior com 2 colunas
    # -------------------------------------
    col_esq, col_dir = st.columns(2)

    with col_esq:
        st.subheader("Todo – D-0 (Coluna Esquerda)")
        if not df.empty:
            # Filtrar ou exibir dados específicos nesta coluna
            st.dataframe(df.head())  # Exemplo: exibe apenas as 5 primeiras linhas
        else:
            st.info("Nenhum dado retornado ou engine não configurada.")

    with col_dir:
        st.subheader("Todo – D-0 (Coluna Direita)")
        if not df.empty:
            # Outro filtro ou visualização diferente
            st.dataframe(df.tail())  # Exemplo: exibe as 5 últimas linhas
        else:
            st.info("Nenhum dado retornado ou engine não configurada.")

