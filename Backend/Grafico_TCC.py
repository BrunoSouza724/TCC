import sqlite3
import matplotlib.pyplot as plt

con = sqlite3.connect('Lancamentos.db')
cursor = con.cursor()

cursor.execute('''
    SELECT Data, Valor FROM Lancamentos 
''')

resultados = cursor.fetchall()
contador = len(resultados)

for dados in resultados:
    print(dados)

print(f'Total de resultados: {contador}')

Data = [dados[0] for dados in resultados] 
Valor = [dados[1] for dados in resultados] 

plt.figure(figsize=(10, 5)) 
plt.bar(Data, Valor, color='blue')

plt.title('Valor cadastrado em 2024')
plt.xlabel('Data')
plt.ylabel('Valor')

plt.xticks(rotation=45, ha='right')

plt.tight_layout()

plt.show()

con.commit()