import streamlit as st
import sqlite3

# Função de conexão com o banco


def conectar_banco():
    return sqlite3.connect('Lancamentos.db')


def Cadastro_Produto():
    # Logo na barra lateral
    st.sidebar.image("logo.png", use_container_width=True)

    st.title("📝 Cadastro de Produtos")

    # Criação da tabela de produtos caso não exista
    con = conectar_banco()
    cursor = con.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE
        )
    ''')
    con.commit()
    con.close()

    if "modo_edicao_produto" not in st.session_state:
        st.session_state["modo_edicao_produto"] = False
    if "produto_para_excluir" not in st.session_state:
        st.session_state["produto_para_excluir"] = None
    if "exibir_confirmacao" not in st.session_state:
        st.session_state["exibir_confirmacao"] = False

    if not st.session_state["modo_edicao_produto"]:
        novo_produto = st.text_input(
            "Digite o nome do produto para cadastrar:")

        if st.button("Salvar Produto"):
            if novo_produto.strip() == "":
                st.error("Por favor, insira um nome de produto.")
            else:
                nome_formatado = novo_produto.strip().capitalize()

                con = conectar_banco()
                cursor = con.cursor()
                cursor.execute(
                    "SELECT COUNT(*) FROM Produtos WHERE LOWER(nome) = LOWER(?)", (nome_formatado,))
                existe = cursor.fetchone()[0]
                con.close()

                if existe:
                    st.error(
                        f"⚠️ O produto '{nome_formatado}' já está cadastrado.")
                else:
                    try:
                        con = conectar_banco()
                        cursor = con.cursor()
                        cursor.execute(
                            "INSERT INTO Produtos (nome) VALUES (?)", (nome_formatado,))
                        con.commit()
                        st.success(
                            f"✅ Produto '{nome_formatado}' cadastrado com sucesso!")
                    except sqlite3.Error as e:
                        st.error(f"Erro ao salvar produto: {e}")
                    finally:
                        con.close()
                        st.rerun()

        st.markdown("---")

    con = conectar_banco()
    cursor = con.cursor()
    cursor.execute("SELECT nome FROM Produtos ORDER BY nome")
    produtos = cursor.fetchall()
    con.close()

    if produtos:
        st.subheader("📋 Produtos Cadastrados")
        col1, col2 = st.columns([0.8, 0.2])

        with col1:
            for p in produtos:
                st.write(p[0])

        with col2:
            if not st.session_state["modo_edicao_produto"]:
                if st.button("✏️ Editar", use_container_width=True):
                    st.session_state["modo_edicao_produto"] = True
                    st.rerun()
            else:
                if st.button("🔙 Voltar", use_container_width=True):
                    st.session_state["modo_edicao_produto"] = False
                    st.session_state["exibir_confirmacao"] = False
                    st.rerun()

        if st.session_state["modo_edicao_produto"]:
            nomes_produtos = [p[0] for p in produtos]
            produto_selecionado = st.selectbox(
                "Selecione um produto para excluir:", nomes_produtos)

            if st.button("❌ Excluir Produto"):
                st.session_state["produto_para_excluir"] = produto_selecionado
                st.session_state["exibir_confirmacao"] = True
                st.rerun()

            if st.session_state["exibir_confirmacao"]:
                col_msg, col_sim, col_cancel = st.columns([0.5, 0.25, 0.25])
                with col_msg:
                    st.warning(
                        f"Tem certeza que deseja excluir o produto **{st.session_state['produto_para_excluir']}**?")
                with col_sim:
                    if st.button("✅ Sim", key="btn_sim"):
                        try:
                            con = conectar_banco()
                            cursor = con.cursor()
                            cursor.execute(
                                "DELETE FROM Produtos WHERE nome = ?", (st.session_state["produto_para_excluir"],))
                            con.commit()
                            st.success(
                                f"✅ Produto '{st.session_state['produto_para_excluir']}' excluído com sucesso!")
                        except sqlite3.Error as e:
                            st.error(f"Erro ao excluir produto: {e}")
                        finally:
                            con.close()
                            st.session_state["exibir_confirmacao"] = False
                            st.session_state["produto_para_excluir"] = None
                            st.rerun()
                with col_cancel:
                    if st.button("❌ Cancelar", key="btn_cancelar"):
                        st.session_state["exibir_confirmacao"] = False
                        st.session_state["produto_para_excluir"] = None
                        st.info("Exclusão cancelada.")
                        st.rerun()
    else:
        st.info("Nenhum produto cadastrado ainda.")
