import streamlit as st
from Teste_Entrada import Teste_Entrada


def main():
    # Inicializar a variável de estado na primeira execução
    if "tela_atual" not in st.session_state:
        st.session_state.tela_atual = "menu"

    # Controle de navegação
    if st.session_state.tela_atual == "menu":
        st.title('Selecione uma opção')

        # Botão para navegar para a tela de entrada/saída
        if st.button(':credit_card: Entrada e Saída'):
            st.session_state.tela_atual = "entrada_saida"

        # Outras opções
        if st.button(':chart: Demonstrações Financeiras'):
            st.info("Funcionalidade em desenvolvimento!")

        if st.button(':moneybag: Resumo Financeiro'):
            st.info("Funcionalidade em desenvolvimento!")

        # Barra lateral
        st.sidebar.image('Logo.png')
        st.sidebar.title(
            'Seja-Bem Vindo ao Controle Financeiro :heavy_dollar_sign:')

    elif st.session_state.tela_atual == "entrada_saida":
        # Chama o componente de entrada e saída
        Teste_Entrada()
        if st.button("Voltar para o menu"):
            st.session_state.tela_atual = "menu"


if __name__ == "__main__":
    main()
