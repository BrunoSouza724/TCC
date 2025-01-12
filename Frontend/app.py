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
        st.button(':credit_card: Entrada e Saída', on_click=lambda: mudar_tela("entrada_saida"))

        # Outras opções
        st.button(':chart: Demonstrações Financeiras', on_click=lambda: st.info("Funcionalidade em desenvolvimento!"))
        st.button(':moneybag: Resumo Financeiro', on_click=lambda: st.info("Funcionalidade em desenvolvimento!"))

        # Barra lateral
        st.sidebar.image('Logo.png')
        st.sidebar.title(
            'Seja-Bem Vindo ao Controle Financeiro :heavy_dollar_sign:'
        )

    elif st.session_state.tela_atual == "entrada_saida":
        # Chama o componente de entrada e saída
        Teste_Entrada()

        # Botão único para voltar ao menu principal
        st.button("Voltar para o menu", on_click=lambda: mudar_tela("menu"))


def mudar_tela(tela):
    """Função para atualizar a tela atual."""
    st.session_state.tela_atual = tela


if __name__ == "__main__":
    main()
