import os
import re
from extrai_texto_pdf import encontrar_texto_com_regiao

tabela_meses = {
    'janeiro': 1,
    'fevereiro': 2,
    'março': 3,
    'abril': 4,
    'maio': 5,
    'junho': 6,
    'julho': 7,
    'agosto': 8,
    'setembro': 9,
    'outubro': 10,
    'novembro': 11,
    'dezembro': 12
}

padrao_re = re.compile("\\d{5}-\\d{3}")
textos_alvo = ["Consumo mês / kWh", "Conta do mês"]

def obter_pdf_source() -> dict:
    while True:
        try:
            print("-------------------------------------------")
            print("Por favor, insira o caminho do arquivo PDF: ")
            arquivo = input("Caminho do PDF: ").strip()
            
            # Verifica se o caminho aponta para um arquivo válido se ele é de extensão .pdf
            if os.path.isfile(arquivo) and arquivo.lower().endswith('.pdf'):
                print("Arquivo PDF encontrado. Processando...")
                # Chama a função de encontrar texto da classe `extrai_texto_pdf`
                texto_extraido:dict = encontrar_texto_com_regiao(arquivo, textos_alvo, padrao_re)
                texto_extraido_corrigido = corrige_mes(texto_extraido)
                print("Texto extraído com sucesso!")
                print("---------------------------\n")
                return texto_extraido_corrigido
            else:
                print("Erro! Por favor, insira um caminho de arquivo PDF válido.")
        except Exception as e:
            print(f"Erro ao extrair o texto! Erro: {e}")
            
            
def corrige_mes(texto_extraido:dict) -> dict:
    aux = []
    aux = texto_extraido['mes_consumo'].split("/")
    mes_ano = f"{tabela_meses[aux[0].lower()]}/{aux[1]}"
    texto_extraido['mes_consumo'] = mes_ano
    return texto_extraido
    