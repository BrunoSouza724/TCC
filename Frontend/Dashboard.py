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
    # Criar uma cópia para não modificar o DataFrame original
    df_saldo = df.copy()
    
    # Converter valores de saída para negativos
    df_saldo['Valor'] = df_saldo.apply(
        lambda row: -row['Valor'] if row['Tipo'] == 'Saída' else row['Valor'], 
        axis=1
    )
    
    # Calcular o saldo acumulado por data
    df_saldo = df_saldo.groupby('Data', as_index=False).agg({'Valor': 'sum'})
    df_saldo['Saldo Acumulado'] = df_saldo['Valor'].cumsum()
    
    return df_saldo

def exibir_graficos(df):
    if not df.empty:
        df['Data'] = pd.to_datetime(df['Data'])
        
        # Gráfico de barras - Valor por Descrição (com cor personalizada)
        fig_bar = px.bar(df, x='Descricao', y='Valor', color='Tipo', 
                         title="Valor por Descrição", 
                         color_discrete_sequence=["#2E8B57"])  # Cor personalizada
        st.plotly_chart(fig_bar)
        
        # Gráfico de linha - Evolução Financeira (agora com saldo acumulado e cor personalizada)
        df_saldo = calcular_saldo_acumulado(df)
        fig_line = px.line(df_saldo, x='Data', y='Saldo Acumulado', 
                           markers=True, title="Evolução do Saldo Financeiro",
                           labels={'Saldo Acumulado': 'Saldo (R$)'},
                           line_shape="linear")
        
        # Adicionar linha horizontal no zero para referência
        fig_line.add_hline(y=0, line_dash="dash", line_color="red")
        
        # Definir a cor da linha
        fig_line.update_traces(line=dict(color="#2E8B57"))  # Cor personalizada para a linha
        st.plotly_chart(fig_line)
    else:
        st.info("Nenhum dado disponível para os filtros selecionados.")

def main():
    st.sidebar.image('Logo.png')
    st.sidebar.title('Seja-Bem Vindo ao Controle Financeiro :heavy_dollar_sign:')
    
    st.title(":moneybag: Resumo Financeiro")
    
    # Filtros
    data, descricao, entrada_saida = st.columns(3)
    
    with data:
        hoje = datetime.date.today()
        periodo_selecionado = st.date_input(
            "Data",
            value=(hoje - datetime.timedelta(days=5), hoje)
        )
        start_date, end_date = (periodo_selecionado if isinstance(periodo_selecionado, tuple) 
                              else (periodo_selecionado, periodo_selecionado))
    
    with descricao:
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
        tipo_transacao = st.radio("Tipo de Transação", ("Entrada", "Saída", "Ambas"))
    
    if st.button("Gerar Gráficos"):
        df = carregar_dados(start_date, end_date, dado_selecionado, tipo_transacao)
        exibir_graficos(df)


if __name__ == "__main__":
    main()
