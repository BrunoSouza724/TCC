import streamlit as st
import pandas as pd
import datetime
import sqlite3

def conectar_banco():
    return sqlite3.connect('Lancamentos.db')

def main():
    st.sidebar.image('Logo.png')
    st.sidebar.title('Seja-Bem Vindo ao Controle Financeiro :heavy_dollar_sign:')

    st.title("Dashboard - Demonstrações Financeiras")

    def voltar_menu():
        st.session_state.tela_atual = "menu"

    # Criação das colunas para os filtros
    data, descricao, entrada_saida = st.columns(3)

    # Botão de Data
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
        # Conectar ao banco e obter os valores únicos da coluna Descricao
        conn = conectar_banco()
        try:
            df_descricoes = pd.read_sql_query("SELECT DISTINCT Descricao FROM Lancamentos", conn)
            opcoes_dados = ["Todos"] + df_descricoes["Descricao"].tolist() if not df_descricoes.empty else ["Nenhuma opção disponível"]
        except Exception as e:
            st.error(f"Erro ao obter descrições do banco de dados: {e}")
            opcoes_dados = ["Erro ao carregar"]
        finally:
            conn.close()

        dado_selecionado = st.selectbox("Selecione a Descrição", opcoes_dados)

    with entrada_saida:
        tipo_transacao = st.radio("Entrada, Saída ou Ambas", ("Entrada", "Saída", "Ambas"))

    # Botão para buscar dados
    if st.button("Buscar Dados"):
        if dado_selecionado == "Todos":
            descricao_filter = ""
        else:
            descricao_filter = f"AND Descricao = '{dado_selecionado}'"

        if tipo_transacao == "Ambas":
            query = f"""
                SELECT Tipo, Data, Data_recebimento, Valor, Metodo
                FROM Lancamentos
                WHERE Data BETWEEN '{start_date}' AND '{end_date}'
                {descricao_filter}
            """
        else:
            query = f"""
                SELECT Tipo, Data, Data_recebimento, Valor, Metodo
                FROM Lancamentos
                WHERE Data BETWEEN '{start_date}' AND '{end_date}'
                {descricao_filter}
                AND Tipo = '{tipo_transacao}'
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

        # Exibe os resultados centralizados
        st.subheader("Resultados da Consulta")
        if not df.empty:
            st.dataframe(df)  # Exibe todos os resultados em uma única tabela centralizada
        else:
            st.info("Nenhum dado retornado ou erro na consulta.")

if __name__ == "__main__":
    main()
