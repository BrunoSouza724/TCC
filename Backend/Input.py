import sqlite3

# Conexão com o banco de dados
con = sqlite3.connect('Lancamentos.db')
cursor = con.cursor()

# Estrutura do menu
print("Selecione uma opção de lançamento:")
print("1. Entrada")
print("2. Saída")
opcao = input("Digite sua opção (1 ou 2): ")

# Determinando o tipo de lançamento
if opcao == "1" or opcao.lower() == "entrada":
    tipo = "Entrada"
elif opcao == "2" or opcao.lower() == "saída":
    tipo = "Saída"
else:
    print("Opção inválida. Tente novamente.")
    con.close()
    exit()

# Coletar dados do usuário
Data = input("Informe a data de operação (YYYY-MM-DD): ")
Data_recebimento = input("Informe a data de recebimento (YYYY-MM-DD): ")
Descricao = input("Informe a descrição do produto/serviço: ")
try:
    Valor = float(input("Informe o valor (use ponto para decimais): "))
except ValueError:
    print("Erro: O valor deve ser um número.")
    con.close()
    exit()

Metodo = input("Informe o método de pagamento: ")

# Inserir os dados no banco
try:
    cursor.execute(
        'INSERT INTO Lancamentos (Tipo, Data, Data_recebimento, Descricao, Valor, Metodo) VALUES (?, ?, ?, ?, ?, ?)',
        (tipo, Data, Data_recebimento, Descricao, Valor, Metodo)
    )
    con.commit()
    print(f'Dados de {tipo} inseridos com sucesso.')
except sqlite3.Error as e:
    print(f"Erro ao inserir dados: {e}")
    con.close()
    exit()

# Fechar a conexão
con.close()
