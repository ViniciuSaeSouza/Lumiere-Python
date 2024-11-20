import pandas as pd
import matplotlib.pyplot as plt

colunas_desejadas = ['Consumo kwh/mês', 'Mês Consumo', 'Data Registro']

def gerar_grafico_consumo(df:pd.DataFrame, usuario_info:dict):
    # Carregar o dataset
    # Filtrar dados de um único usuário para análise
    usuario_nome:str = usuario_info['nome']
    
    df_usuario = df[colunas_desejadas]

    # Calcular a média de consumo dos três primeiros meses
    media_base = df_usuario['Consumo kwh/mês'].iloc[:3].mean()

    # Adicionar uma coluna indicando se o consumo está acima ou abaixo da média
    df_usuario.loc[:, 'Status'] = df_usuario['Consumo kwh/mês'].apply(lambda x: 'Acima' if x > media_base else 'Abaixo')

    # Plotar o gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(df_usuario['Mês Consumo'], df_usuario['Consumo kwh/mês'], marker='o', color='grey', label='Consumo Mensal')
    plt.axhline(y=media_base, color='red', linestyle='--', label=f'Média dos 3 primeiros meses ({media_base:.2f} kWh)')

    # Destacar os pontos acima e abaixo da média
    for i, row in df_usuario.iterrows():
        color = 'green' if row['Status'] == 'Abaixo' else 'red'
        plt.plot(row['Mês Consumo'], row['Consumo kwh/mês'], marker='o', color=color)

    # Configurações do gráfico
    plt.title(f'Consumo Mensal de {usuario_nome.capitalize()}')
    plt.xlabel('Mês')
    plt.ylabel('Consumo (kWh)')
    plt.legend()
    plt.grid(True)
    plt.show()
