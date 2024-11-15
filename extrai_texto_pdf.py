import fitz  # PyMuPDF
import re
# Recebe o caminho do arquivo pdf a ser lido, o texto_alvo a ser encontrado e a margem que define o tamanho do bloco de procura em volta do texto_alvo
def encontrar_texto_com_regiao(pdf_path:str, textos_alvo:list, padrao_re:str, margem=15) -> dict:
    try:
        # Abre o PDF
        doc = fitz.open(pdf_path)
        # Inicia um dicionário vazio para guardar os resultados de todos os textos_alvos | padrao_re passados
        resultados = {
            'consumo': 0,
            'data_conta': '',
            'cep' : ''
        }
        pagina = doc.load_page(0)
        texto_pagina = pagina.get_text("text")
        
        # Procura o texto alvo e obtém as coordenadas de sua posição
        if texto_pagina:
            
            for alvo in textos_alvo:
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
                    
                    match alvo:
                        case "Conta do mês":
                            resultados["data_conta"] = texto_area.strip()[27:]
                        case "Consumo mês / kWh":
                            resultados["consumo"] = int((texto_area[-4:]).strip())
                            
            # Procura por qualquer item que atenda ao padrão regex (padrao_re), padrão para cep definido como r"\d{5}-\d{3}" = xxxxx-xxx
            padroes_encontrados = re.findall(padrao_re, texto_pagina)
            resultados["cep"] = padroes_encontrados[0]
        
        # Verifica se o algum valor não foi encontrado na extração e informa no terminal
        for k, v in resultados.items():
            if not v:
                print(f"Não foi possível achar o {k}...")
            else:
                print(f"{k.capitalize()}...: {v}")
        
        # Fecha o arquivo
        doc.close()

        return resultados
    except ValueError as e:
        print('Erro')
    

# Uso do código / Teste do código
# pdf_path = "fitz/conta-ma.pdf"
# textos_alvo = ["Consumo mês / kWh", "Conta do mês"]
# padrao_cep = re.compile("\\d{5}-\\d{3}") # Padrão regex para encontrar cep no pdf
# margem = 15  # Ajuste a margem conforme necessário
# resultados = encontrar_texto_com_regiao(pdf_path, textos_alvo, padrao_cep, margem)



