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
            SELECT Data, Descricao, Quantidade, Valor, (Quantidade * Valor) as ValorTotal, Tipo
            FROM Lancamentos
            WHERE Data BETWEEN '{start_date}' AND '{end_date}'
            {descricao_filter} {tipo_filter}
            ORDER BY Data
        """

        df = pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"Erro ao consultar o banco de dados: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()

    return df


def calcular_saldo_acumulado(df):
    df_saldo = df.copy()
    # ENTRADA como negativa, SAÍDA como positiva
    df_saldo['ValorTotal'] = df_saldo.apply(
        lambda row: -
        row['ValorTotal'] if row['Tipo'] == 'Entrada' else row['ValorTotal'],
        axis=1
    )
    df_saldo = df_saldo.groupby(
        'Data', as_index=False).agg({'ValorTotal': 'sum'})
    df_saldo['Saldo Acumulado'] = df_saldo['ValorTotal'].cumsum()
    return df_saldo


def exibir_graficos(df, df_saldo):
    if not df.empty:
        df['Data'] = pd.to_datetime(df['Data'])
        df_saldo['Data'] = pd.to_datetime(df_saldo['Data'])

        # Saldo final
        saldo_final = df_saldo['Saldo Acumulado'].iloc[-1]
        st.metric("💰 Saldo Final do Período", f"R$ {saldo_final:,.2f}")

        # Gráfico de barras - Valor Total por Descrição
        fig_bar = px.bar(
            df,
            x='Descricao',
            y='ValorTotal',
            color='Tipo',
            title="Valor Total por Descrição",
            text='ValorTotal',
            color_discrete_map={
                "Entrada": "#B22222",  # Vermelho para entradas (negativo)
                "Saída": "#2E8B57"     # Verde para saídas (positivo)
            }
        )
        fig_bar.update_traces(
            texttemplate='%{text:.2f}', textposition='outside')
        fig_bar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        st.plotly_chart(fig_bar)

        # Gráfico de linha - Evolução do Saldo Acumulado
        fig_line = px.line(
            df_saldo,
            x='Data',
            y='Saldo Acumulado',
            markers=True,
            title="Evolução do Saldo Financeiro",
            labels={'Saldo Acumulado': 'Saldo (R$)'},
            line_shape="linear"
        )
        fig_line.add_hline(y=0, line_dash="dash", line_color="red")
        fig_line.update_traces(line=dict(color="#2E8B57"))
        fig_line.update_layout(yaxis_tickprefix="R$ ")
        st.plotly_chart(fig_line)
    else:
        st.info("Nenhum dado disponível para os filtros selecionados.")


def main():
    st.sidebar.image('Logo.png')
    st.sidebar.title(
        'Seja-Bem Vindo ao Controle Financeiro :heavy_dollar_sign:')
    st.title(":bar_chart: Gráficos")

    data, descricao, entrada_saida = st.columns(3)

    with data:
        hoje = datetime.date.today()
        periodo_selecionado = st.date_input(
            "Período", value=(hoje - datetime.timedelta(days=5), hoje))
        if isinstance(periodo_selecionado, tuple) and len(periodo_selecionado) == 2:
            start_date, end_date = periodo_selecionado
        else:
            start_date = end_date = periodo_selecionado

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
        df_saldo = calcular_saldo_acumulado(df)
        exibir_graficos(df, df_saldo)


if __name__ == "__main__":
    main()
