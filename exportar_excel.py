import pandas as pd
from datetime import datetime
dia = datetime.now().day
mes = datetime.now().month
ano = datetime.now().year
data_atual = f"{ano}_{mes}_{dia}"
def exportar_para_excel(df: pd.DataFrame, nome_arquivo: str = f'relatorio_consumo_{data_atual}.xlsx'):
    try:
        # Exporta o DataFrame para um arquivo Excel
        df.to_excel(nome_arquivo, index=False)
        print(f"Dados exportados com sucesso para {nome_arquivo}")
    except Exception as e:
        print(f"Ocorreu um erro ao exportar para Excel: {e}")