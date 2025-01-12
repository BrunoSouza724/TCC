import streamlit as st

def Teste_Entrada():
    st.title(':credit_card: Entrada e Saída')

    # Inicializar valores no session_state na primeira execução
    if "formulario_visivel" not in st.session_state:
        st.session_state.formulario_visivel = True
    if "salvo" not in st.session_state:
        st.session_state.salvo = False
    if "dados_transacao" not in st.session_state:
        st.session_state.dados_transacao = {}
    if "tela_atual" not in st.session_state:
        st.session_state.tela_atual = "entrada_saida"

    # Funções para gerenciar os botões
    def salvar_transacao():
        if st.session_state.dados_transacao["descricao"]:
            st.session_state.formulario_visivel = False
            st.session_state.salvo = True
        else:
            st.error("Por favor, selecione ao menos uma descrição.")

    def nova_transacao():
        st.session_state.formulario_visivel = True
        st.session_state.salvo = False
        st.session_state.dados_transacao = {}

    def voltar_menu():
        st.session_state.tela_atual = "menu"

    # Controle da navegação
    if st.session_state.tela_atual == "entrada_saida":
        if st.session_state.formulario_visivel:
            # Campos do formulário
            st.session_state.dados_transacao["tipo"] = st.radio(
                "Tipo de transação:", ["Entrada", "Saída"], horizontal=True, key="tipo"
            )
            st.session_state.dados_transacao["data"] = st.date_input("Data da transação:", key="data")
            st.session_state.dados_transacao["data_recebimento_pagamento"] = st.date_input(
                "Data de Recebimento/Pagamento:", key="data_recebimento_pagamento"
            )
            st.session_state.dados_transacao["descricao"] = st.multiselect(
                "Descrição (Selecione um ou mais itens):",
                ["Caneta", "Lápis", "Caderno"],
                key="descricao"
            )
            st.session_state.dados_transacao["valor"] = st.number_input(
                "Valor da transação:", min_value=0.0, step=0.01, format="%.2f", key="valor"
            )
            st.session_state.dados_transacao["metodo"] = st.selectbox(
                "Método de pagamento:", ["Dinheiro", "Cartão de Crédito", "Cartão de Débito"], key="metodo"
            )

            # Botão de salvar
            st.button("Salvar transação", on_click=salvar_transacao)

        if st.session_state.salvo and not st.session_state.formulario_visivel:
            dados = st.session_state.dados_transacao
            st.write("### Detalhes da Transação")
            st.write(f"**Tipo:** {dados['tipo']}")
            st.write(f"**Data:** {dados['data']}")
            st.write(f"**Data de Recebimento/Pagamento:** {dados['data_recebimento_pagamento']}")
            st.write(f"**Descrição:** {', '.join(dados['descricao'])}")
            st.write(f"**Valor:** R$ {dados['valor']:.2f}")
            st.write(f"**Método:** {dados['metodo']}")

            # Botão para iniciar uma nova transação
            st.button("Nova transação", on_click=nova_transacao)

             # Barra lateral
        st.sidebar.image('Logo.png')
        st.sidebar.title(
            'Seja-Bem Vindo ao Controle Financeiro :heavy_dollar_sign:'
        )
