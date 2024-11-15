import fitz  # PyMuPDF
import re
# Recebe o caminho do arquivo pdf a ser lido, o texto_alvo a ser encontrado e a margem que define o tamanho do bloco de procura em volta do texto_alvo
def encontrar_texto_com_regiao(pdf_path:str, texto_alvo:str=None, padrao_re:str=None, margem=50) -> dict:
    # Abre o PDF
    doc = fitz.open(pdf_path)
    # Inicia uma lista vazia para guardar os resultados de todos os textos_alvos passados
    resultados = {
        "consumo" : 'None',
        "cep" : 'None',
        "data_conta" : 'None',
    }
    pagina = doc.load_page(0)
    texto_pagina = pagina.get_text("text")
    
    # Procura o texto alvo e obtém as coordenadas de sua posição
    for alvo in texto_alvo:
        ocorrencias = pagina.search_for(alvo)
        # Calcula a área ao redor do texto alvo (usando a margem)
        for ocr in ocorrencias:
            area = fitz.Rect(
                ocr.x0 - margem,
                ocr.y0 - margem,
                ocr.x1 + margem,
                ocr.y1 + margem
            )
            # Extrai o texto na área definida
            texto_area = pagina.get_text("text", clip=area)
            if alvo == "Conta do mês":
                resultados["data_conta"] = texto_area.strip()[27:]
            else:
                resultados["consumo"] = (texto_area[-4:]).strip()
        
        # Procura por qualquer item que atenda ao padrão regex (padrao_re), padrão para cep definido como r"\d{5}-\d{3}"
        padroes_encontrados = re.findall(padrao_re, texto_pagina)
        if padroes_encontrados:
            resultados["cep"] = padroes_encontrados[0]
    
    doc.close()
    return resultados

# Uso do código
pdf_path = "opencv/contapdf.png"
texto_alvo = ["Consumo mês / kWh", "Conta do mês"]
padrao_re = re.compile("\\d{5}-\\d{3}") # Padrão regex para encontrar cep no pdf
margem = 15  # Ajuste a margem conforme necessário
try:
    resultados = encontrar_texto_com_regiao(pdf_path, texto_alvo, padrao_re, margem)
    acc = 0
    for k, v in resultados.items():
        if v == 'None':
            print(f"Falha ao achar {k}..." )

    # Exibe os resultados
    print("Consumo: " + resultados["consumo"])
    print("Cep: " + resultados["cep"])
    print("Data: "+ resultados["data_conta"])
except fitz.FileNotFoundError as e:
    print("Erro ao abrir o arquivo, arquivo não existe!")
except ValueError as e:
    print(e)


