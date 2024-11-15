import pandas as pd
import matplotlib.pyplot as plt

# Carregar o dataset
df = pd.read_csv('matplot/consumo_energia.csv')

# Filtrar dados de um único usuário para análise
usuario_id = 1
df_usuario = df[df['ID_usuario'] == usuario_id]

# Calcular a média de consumo dos três primeiros meses
media_base = df_usuario['Consumo_mensal_kWh'].iloc[:3].mean()

# Adicionar uma coluna indicando se o consumo está acima ou abaixo da média
df_usuario['Status'] = df_usuario['Consumo_mensal_kWh'].apply(lambda x: 'Acima' if x > media_base else 'Abaixo')

# Plotar o gráfico
plt.figure(figsize=(10, 6))
plt.plot(df_usuario['Mês'], df_usuario['Consumo_mensal_kWh'], marker='o', color='blue', label='Consumo Mensal')
plt.axhline(y=media_base, color='red', linestyle='--', label=f'Média dos 3 primeiros meses ({media_base:.2f} kWh)')

# Destacar os pontos acima e abaixo da média
for i, row in df_usuario.iterrows():
    color = 'green' if row['Status'] == 'Abaixo' else 'orange'
    plt.plot(row['Mês'], row['Consumo_mensal_kWh'], marker='o', color=color)

# Configurações do gráfico
plt.title(f'Consumo Mensal do Usuário {usuario_id}')
plt.xlabel('Mês')
plt.ylabel('Consumo (kWh)')
plt.legend()
plt.grid(True)
plt.show()
