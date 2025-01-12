import streamlit as st

def main():
    st.title('Selecione uma opção')
    container = st.container(border=True)
    container.write(':credit_card: Entrada e Saída')
    container = st.container(border=True)
    container.write(':chart: Demonstrações Financeiras')
    container = st.container(border=True)
    container.write(':moneybag: Resumo Financeiro')
    
    st.sidebar.image('Logo.png')
    st.sidebar.title('Seja-Bem Vindo ao Controle Financeiro :heavy_dollar_sign:')
   
if __name__ == "__main__":
    main()
