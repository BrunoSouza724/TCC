import streamlit as st
import pandas as pd
import datetime
import sqlite3
import plotly.express as px


def conectar_banco():
    return sqlite3.connect('Lancamentos.db')


def carregar_dados(start_date, end_date, descricao, tipo_transacao):
    conn = conectar_banco()
    try:
        descricao_filter = "" if descricao == "Todos" else f"AND Descricao = '{descricao}'"
        tipo_filter = "" if tipo_transacao == "Ambas" else f"AND Tipo = '{tipo_transacao}'"

        query = f"""
            SELECT Data, Descricao, Valor, Tipo
            FROM Lancamentos
            WHERE Data BETWEEN '{start_date}' AND '{end_date}'
            {descricao_filter} {tipo_filter}
        """

        df = pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"Erro ao consultar o banco de dados: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()

    return df


def exibir_graficos(df):
    if not df.empty:
        df['Data'] = pd.to_datetime(df['Data'])

        # Gráfico de barras - Valor por Descrição
        fig_bar = px.bar(df, x='Descricao', y='Valor',
                         color='Tipo', title="Valor por Descrição")
        st.plotly_chart(fig_bar)

        # Gráfico de linha - Evolução Financeira
        fig_line = px.line(df, x='Data', y='Valor', color='Tipo',
                           markers=True, title="Evolução Financeira")
        st.plotly_chart(fig_line)
    else:
        st.info("Nenhum dado disponível para os filtros selecionados.")


def main():
    st.sidebar.image('Logo.png')
    st.sidebar.title('Dashboard Financeiro :moneybag:')

    st.title("Dashboard - Análises Financeiras")

    # Filtros
    data, descricao, entrada_saida = st.columns(3)

    with data:
        periodo_selecionado = st.date_input("Data", value=(
            datetime.date(2025, 1, 1), datetime.date(2025, 1, 20)))
        start_date, end_date = (periodo_selecionado if isinstance(
            periodo_selecionado, tuple) else (periodo_selecionado, periodo_selecionado))

    with descricao:
        conn = conectar_banco()
        try:
            df_descricoes = pd.read_sql_query(
                "SELECT DISTINCT Descricao FROM Lancamentos", conn)
            opcoes_dados = ["Todos"] + df_descricoes["Descricao"].tolist(
            ) if not df_descricoes.empty else ["Nenhuma opção disponível"]
        except Exception as e:
            st.error(f"Erro ao obter descrições do banco de dados: {e}")
            opcoes_dados = ["Erro ao carregar"]
        finally:
            conn.close()

        dado_selecionado = st.selectbox("Selecione a Descrição", opcoes_dados)

    with entrada_saida:
        tipo_transacao = st.radio(
            "Tipo de Transação", ("Entrada", "Saída", "Ambas"))

    if st.button("Gerar Gráficos"):
        df = carregar_dados(start_date, end_date,
                            dado_selecionado, tipo_transacao)
        exibir_graficos(df)


if __name__ == "__main__":
    main()
