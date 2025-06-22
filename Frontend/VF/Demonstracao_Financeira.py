import streamlit as st
import pandas as pd
import datetime
import sqlite3
import io


def conectar_banco():
    return sqlite3.connect('Lancamentos.db')


def excluir_lancamento(lancamento_id):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Lancamentos WHERE id = ?",
                       (lancamento_id,))
        conn.commit()
        st.success(f"Lançamento {lancamento_id} removido com sucesso.")
    except Exception as e:
        st.error(f"Erro ao excluir lançamento: {e}")
    finally:
        conn.close()


def atualizar_lancamento(lancamento_id, novo_valor, nova_quantidade):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("UPDATE Lancamentos SET Valor = ?, Quantidade = ? WHERE id = ?",
                       (novo_valor, nova_quantidade, lancamento_id))
        conn.commit()
        st.success(f"Lançamento {lancamento_id} atualizado.")
    except Exception as e:
        st.error(f"Erro ao atualizar: {e}")
    finally:
        conn.close()


def buscar_dados(start_date, end_date, dado_selecionado, tipo_transacao):
    if dado_selecionado == "Todos":
        descricao_filter = ""
    else:
        descricao_filter = f"AND Descricao = '{dado_selecionado}'"

    if tipo_transacao == "Ambas":
        query = f"""
            SELECT id, Tipo, Data, Descricao, Quantidade, Valor, (Quantidade * Valor) as ValorTotal, Metodo
            FROM Lancamentos
            WHERE Data BETWEEN '{start_date}' AND '{end_date}'
            {descricao_filter}
        """
    else:
        query = f"""
            SELECT id, Tipo, Data, Descricao, Quantidade, Valor, (Quantidade * Valor) as ValorTotal, Metodo
            FROM Lancamentos
            WHERE Data BETWEEN '{start_date}' AND '{end_date}'
            {descricao_filter}
            AND Tipo = '{tipo_transacao}'
        """

    conn = conectar_banco()
    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"Erro na consulta: {e}")
        df = pd.DataFrame()
    finally:
        conn.close()

    return df


def gerar_excel_formatado(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Relatório')
        workbook = writer.book
        worksheet = writer.sheets['Relatório']

        # Formatação para cabeçalhos
        header_format = workbook.add_format(
            {'bold': True, 'bg_color': '#D9E1F2', 'border': 1})
        currency_format = workbook.add_format({'num_format': 'R$ #,##0.00'})

        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 15)

        # Aplicar formatação monetária nas colunas de valores, se existirem
        colunas = df.columns.tolist()
        if "Valor Unitário" in colunas:
            idx = colunas.index("Valor Unitário")
            worksheet.set_column(idx, idx, 15, currency_format)
        if "Valor Total" in colunas:
            idx = colunas.index("Valor Total")
            worksheet.set_column(idx, idx, 18, currency_format)

    output.seek(0)
    return output


def main():
    st.sidebar.image('Logo.png')
    st.sidebar.title(
        'Seja-Bem Vindo ao Controle Financeiro :heavy_dollar_sign:')

    st.title(":page_facing_up: Relatórios Financeiros")

    if "modo_edicao" not in st.session_state:
        st.session_state.modo_edicao = False
    if "df_resultado" not in st.session_state:
        st.session_state.df_resultado = pd.DataFrame()
    if "confirmacoes" not in st.session_state:
        st.session_state.confirmacoes = {}
    if "novos_valores" not in st.session_state:
        st.session_state.novos_valores = {}
    if "novas_quantidades" not in st.session_state:
        st.session_state.novas_quantidades = {}

    data, descricao, entrada_saida = st.columns(3)

    with data:
        hoje = datetime.date.today()
        cinco_dias_atras = hoje - datetime.timedelta(days=4)
        periodo_selecionado = st.date_input(
            "Data", value=(cinco_dias_atras, hoje))

        if isinstance(periodo_selecionado, tuple) and len(periodo_selecionado) == 2:
            start_date, end_date = periodo_selecionado
        else:
            start_date = periodo_selecionado
            end_date = periodo_selecionado

    with descricao:
        conn = conectar_banco()
        try:
            df_descricoes = pd.read_sql_query(
                "SELECT DISTINCT Descricao FROM Lancamentos", conn)
            opcoes_dados = ["Todos"] + df_descricoes["Descricao"].tolist(
            ) if not df_descricoes.empty else ["Nenhuma opção disponível"]
        except Exception as e:
            st.error(f"Erro ao obter descrições: {e}")
            opcoes_dados = ["Erro ao carregar"]
        finally:
            conn.close()

        dado_selecionado = st.selectbox("Selecione a Descrição", opcoes_dados)

    with entrada_saida:
        tipo_transacao = st.radio(
            "Entrada, Saída ou Ambas", ("Entrada", "Saída", "Ambas"))

    if st.button("Buscar Dados"):
        df = buscar_dados(start_date, end_date,
                          dado_selecionado, tipo_transacao)
        if not df.empty:
            st.session_state.df_resultado = df
            st.session_state.novos_valores = {}
            st.session_state.novas_quantidades = {}
        else:
            st.info("Nenhum dado retornado ou erro na consulta.")
            st.session_state.df_resultado = pd.DataFrame()

    if not st.session_state.df_resultado.empty:
        col_titulo, col_botao = st.columns([7, 2])
        with col_titulo:
            st.subheader("Resultados da Consulta")
        with col_botao:
            if not st.session_state.modo_edicao:
                if st.button("✏️ Editar"):
                    st.session_state.modo_edicao = True
                    st.rerun()
            else:
                if st.button("🔙 Voltar"):
                    st.session_state.modo_edicao = False
                    df_atualizado = buscar_dados(
                        start_date, end_date, dado_selecionado, tipo_transacao)
                    st.session_state.df_resultado = df_atualizado
                    st.rerun()

        if not st.session_state.modo_edicao:
            df_mostrar = st.session_state.df_resultado.copy()
            df_mostrar = df_mostrar[[
                "Descricao", "Tipo", "Data", "Quantidade", "Valor", "ValorTotal", "Metodo"]]
            df_mostrar.rename(columns={
                "Descricao": "Descrição",
                "Tipo": "Tipo",
                "Data": "Data",
                "Quantidade": "Quantidade",
                "Valor": "Valor Unitário",
                "ValorTotal": "Valor Total",
                "Metodo": "Método"
            }, inplace=True)
            df_mostrar.reset_index(drop=True, inplace=True)

            # Formata valores monetários como string
            df_mostrar["Valor Unitário"] = df_mostrar["Valor Unitário"].apply(
                lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            df_mostrar["Valor Total"] = df_mostrar["Valor Total"].apply(
                lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

            st.dataframe(df_mostrar)

            # Botão para baixar Excel formatado
            excel_file = gerar_excel_formatado(df_mostrar)
            st.download_button(
                label="📅 Baixar para o Excel",
                data=excel_file,
                file_name="relatorio_financeiro.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    if st.session_state.modo_edicao:
        st.subheader("Editar Lançamentos")
        for index, row in st.session_state.df_resultado.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([5, 2, 2, 1])
                with col1:
                    st.markdown(f"**Descrição:** {row['Descricao']} | **Tipo:** {row['Tipo']} | "
                                f"**Data:** {row['Data']} | **Método:** {row['Metodo']}")
                with col2:
                    quantidade_valor = int(row['Quantidade']) if pd.notna(
                        row['Quantidade']) else 0
                    quantidade = st.number_input(
                        "Quantidade", min_value=0, step=1, value=quantidade_valor, key=f"quant_{row['id']}")
                    st.session_state.novas_quantidades[row['id']] = quantidade
                with col3:
                    novo_valor_str = st.text_input(
                        "Valor Unitário (R$)", value=f"{float(row['Valor']):.2f}", key=f"valor_{row['id']}")
                    try:
                        novo_valor = float(novo_valor_str.replace(',', '.'))
                    except ValueError:
                        novo_valor = float(row['Valor'])
                    st.session_state.novos_valores[row['id']] = novo_valor
                with col4:
                    if not st.session_state.confirmacoes.get(row['id'], False):
                        if st.button("🗑️", key=f"remover_{row['id']}"):
                            st.session_state.confirmacoes[row['id']] = True
                            st.rerun()

            valor_total = st.session_state.novos_valores[row['id']
                                                         ] * st.session_state.novas_quantidades[row['id']]
            st.write(f"**Valor Total:** R$ {valor_total:.2f}")

            if st.session_state.confirmacoes.get(row['id'], False):
                confirm_col1, confirm_col2, confirm_col3 = st.columns(
                    [0.3, 0.2, 0.2])
                with confirm_col1:
                    st.warning("Tem certeza que deseja excluir?")
                with confirm_col2:
                    if st.button("✅ Sim", key=f"sim_{row['id']}"):
                        excluir_lancamento(row['id'])
                        st.session_state.df_resultado = st.session_state.df_resultado[
                            st.session_state.df_resultado['id'] != row['id']]
                        del st.session_state.confirmacoes[row['id']]
                        st.rerun()
                with confirm_col3:
                    if st.button("❌ Cancelar", key=f"cancelar_{row['id']}"):
                        del st.session_state.confirmacoes[row['id']]
                        st.rerun()

        if st.button("📂 Salvar Alterações"):
            for lancamento_id in st.session_state.novos_valores.keys():
                atualizar_lancamento(
                    lancamento_id,
                    st.session_state.novos_valores[lancamento_id],
                    st.session_state.novas_quantidades[lancamento_id]
                )
            st.success("Todos os lançamentos atualizados com sucesso.")
            st.session_state.modo_edicao = False
            df_atualizado = buscar_dados(
                start_date, end_date, dado_selecionado, tipo_transacao)
            st.session_state.df_resultado = df_atualizado
            st.rerun()


if __name__ == "__main__":
    main()
