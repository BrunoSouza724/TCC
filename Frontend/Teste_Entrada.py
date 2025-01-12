import streamlit as st

def Teste_Entrada():
    st.title(':credit_card: Entrada e Saída')

    # Inicializar valores no session_state apenas na primeira execução
    if "formulario_visivel" not in st.session_state:
        st.session_state.formulario_visivel = True
        st.session_state.salvo = False

        # Inicializar valores padrão
        if "tipo" not in st.session_state:
            st.session_state.tipo = "Entrada"
        if "data" not in st.session_state:
            st.session_state.data = None
        if "data_recebimento_pagamento" not in st.session_state:
            st.session_state.data_recebimento_pagamento = None
        if "descricao" not in st.session_state:
            st.session_state.descricao = []
        if "valor" not in st.session_state:
            st.session_state.valor = 0.0
        if "metodo" not in st.session_state:
            st.session_state.metodo = "Dinheiro"

    # Se o formulário estiver visível
    if st.session_state.formulario_visivel:
        # Tipo: Entrada ou Saída
        st.radio(
            "Tipo de transação:", 
            ["Entrada", "Saída"], 
            horizontal=True, 
            key="tipo"
        )

        # Data
        st.date_input(
            "Data da transação:", 
            key="data"
        )

        # Data de Recebimento/Pagamento
        st.date_input(
            "Data de Recebimento/Pagamento:", 
            key="data_recebimento_pagamento"
        )

        # Descrição
        st.multiselect(
            "Descrição (Selecione um ou mais itens):", 
            ["Caneta", "Lápis", "Caderno"], 
            default=st.session_state.descricao, 
            key="descricao"
        )

        # Valor
        st.number_input(
            "Valor da transação:", 
            min_value=0.0, 
            step=0.01, 
            format="%.2f", 
            key="valor"
        )

        # Método de pagamento
        st.selectbox(
            "Método de pagamento:", 
            ["Dinheiro", "Cartão de Crédito", "Cartão de Débito"], 
            key="metodo"
        )

        # Botão para salvar
        if st.button("Salvar transação"):
            if st.session_state.descricao:
                st.session_state.salvo = True
                st.session_state.formulario_visivel = False  # Oculta o formulário
                st.success("Transação salva com sucesso!")
            else:
                st.error("Por favor, selecione ao menos uma descrição.")

    # Mostrar detalhes da transação salva
    if st.session_state.salvo and not st.session_state.formulario_visivel:
        st.write("### Detalhes da Transação")
        st.write(f"**Tipo:** {st.session_state.tipo}")
        st.write(f"**Data:** {st.session_state.data}")
        st.write(f"**Data de Recebimento/Pagamento:** {st.session_state.data_recebimento_pagamento}")
        st.write(f"**Descrição:** {', '.join(st.session_state.descricao)}")
        st.write(f"**Valor:** R$ {st.session_state.valor:.2f}")
        st.write(f"**Método:** {st.session_state.metodo}")
        if st.button("Nova transação"):
            st.session_state.formulario_visivel = True  # Mostra o formulário novamente
            st.session_state.salvo = False
