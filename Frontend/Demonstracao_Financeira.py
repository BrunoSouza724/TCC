import streamlit as st
import pandas as pd
import datetime
import sqlite3

# Barra lateral
st.sidebar.image('Logo.png')
st.sidebar.title('Seja-Bem Vindo ao Controle Financeiro :heavy_dollar_sign:')

# Função para conexão com o banco de dados SQLite
def conectar_banco():
    return sqlite3.connect('Lancamentos.db')

st.title("Dashboard - Demonstrações Financeiras")


# Criação das colunas para os filtros
data, descricao, entrada_saida = st.columns(3)

#Botão de Data
with data:
    periodo_selecionado = st.date_input(
        "Data",
        value=(datetime.date(2025, 1, 1), datetime.date(2025, 1, 20))
    )
    if isinstance(periodo_selecionado, tuple) and len(periodo_selecionado) == 2:
        start_date, end_date = periodo_selecionado
    else:
        start_date = periodo_selecionado
        end_date = periodo_selecionado

with descricao:
    opcoes_dados = ["coluna1", "coluna2", "coluna3"]
    dado_selecionado = st.selectbox("Selecione o dado desejado", opcoes_dados)

with entrada_saida:
    tipo_transacao = st.radio("Entrada, Saída ou Ambas", ("Entrada", "Saída", "Ambas"))

# Botão para buscar dados
if st.button("Buscar Dados"):
    if tipo_transacao == "Ambas":
        query = f"""
            SELECT *
            FROM Lancamentos.db
            WHERE data BETWEEN '{start_date}' AND '{end_date}'
              AND {dado_selecionado} IS NOT NULL
        """
    else:
        query = f"""
            SELECT *
            FROM Lancamentos.db
            WHERE data BETWEEN '{start_date}' AND '{end_date}'
              AND {dado_selecionado} IS NOT NULL
              AND transacao = '{tipo_transacao}'
        """

    # Conecta ao banco e executa a query
    conn = conectar_banco()
    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"Erro ao consultar o banco de dados: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()

    # Exibe os resultados em duas colunas
    col_esq, col_dir = st.columns(2)

    with col_esq:
        st.subheader("Todo – D-0 (Coluna Esquerda)")
        if not df.empty:
            st.dataframe(df.head())  # Exemplo: exibe as 5 primeiras linhas
        else:
            st.info("Nenhum dado retornado ou erro na consulta.")

    with col_dir:
        st.subheader("Todo – D-0 (Coluna Direita)")
        if not df.empty:
            st.dataframe(df.tail())  # Exemplo: exibe as 5 últimas linhas
        else:
            st.info("Nenhum dado retornado ou erro na consulta.")
