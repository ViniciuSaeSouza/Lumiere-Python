# 558843 - Laura de Oliveira Cintra - 1TDSPK
# 558832 - Maria Eduarda Alves da Paixão - 1TDSPK
# 554456 - Vinícius Saes de Souza - 1TDSPK
from extrai_texto_pdf import encontrar_texto_com_regiao
import os
# import pandas as pd
# from datetime import datetime
import re
from cria_conexao import recupera_conexao

# Variáveis e recusros globais
titulos =  {
    #TÍTULO LUMIERE
    'lumiere':"""
██╗░░░░░  ██╗░░░██╗  ███╗░░░███╗  ██╗  ███████╗  ██████╗░  ███████╗
██║░░░░░  ██║░░░██║  ████╗░████║  ██║  ██╔════╝  ██╔══██╗  ██╔════╝
██║░░░░░  ██║░░░██║  ██╔████╔██║  ██║  █████╗░░  ██████╔╝  █████╗░░
██║░░░░░  ██║░░░██║  ██║╚██╔╝██║  ██║  ██╔══╝░░  ██╔══██╗  ██╔══╝░░
███████╗  ╚██████╔╝  ██║░╚═╝░██║  ██║  ███████╗  ██║░░██║  ███████╗
╚══════╝  ░╚═════╝░  ╚═╝░░░░░╚═╝  ╚═╝  ╚══════╝  ╚═╝░░╚═╝  ╚══════╝
"""
}
padroes_re = {
    "nome" : r"^[a-zA-Z]+( [a-zA-Z]+)*$",
    "email" : r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
}

# Funçõs e Rotinas

def limpa_tela():
    os.system('cls' if os.name == 'Nt' else 'clear')

def finaliza_programa():
    limpa_tela()
    print("Obrigado por usar o Lumiere! \nFinalizando o programa....")
    exit()

# Tenta recuperar uma conexao com o banco de dados da classe `cria_conexao`, se conseguir, cria um cursor para executar instruções SQL, se não, limpa o terminal de acordo com o sistema operacional
try:
    conn = recupera_conexao()
    inst_sql = conn.cursor()
except Exception as e:
    limpa_tela()
    print(f"\t***ERRO*** \n- Ops! infelizmente tivemos uma falha ao recuperar a conexao com o banco de dados!\n- Verifique a conexão com o Banco de Dados Oracle no arquivo `cria_conexao` ou acione o autor do código! \n- Sentimos muito por isso! :(")
    input("Pressione qualquer tecla para sair do programa: ")
    conn.close()
    finaliza_programa()
    


# Recebe um texto:titulo como parâmetro e mostra no terminal
def mostra_titulo(titulo:str):
    tam = len(titulo)
    print('**' * (tam + 2))
    print(f"{" " * (tam // 2)}--{titulo.upper()}--")
    print('**' * (tam + 2))


def valida_formato(padrao:str, texto:str) -> bool:
    if re.match(padroes_re[padrao], texto):
        return True
    else:
        return False
    
def valida_email_existente(email:str) -> list:
    try:
        sql = f"SELECT * FROM tbl_usuarios_py WHERE email = :email"
        inst_sql.execute(sql, (email,))
        data = inst_sql.fetchall()
        
        return data if data else []
    except Exception as e:
        print(f"Falha ao validar o e-mail! ERRO: {e}")
        return []
        
def login():
    limpa_tela()
    login_info = {
        'nome' : '',
        'email' : '',
        'senha': '',
    }
    mostra_titulo("login")
    try:
        while True:
            email = input("Email: ")
            if valida_formato("email", email):
                data = valida_email_existente(email)
                if data:
                    login_info['nome'] = data[0][1]
                    login_info['email'] = data[0][2]
                    login_info['senha'] = data[0][3]
                    print(login_info)
                else:
                    print("E-mail incorreto ou não cadastrado! Digite novamente.")
            else:
                print("Formato do email inválido!")
    except Exception as e:
        print(f"ERRO: {e}")

def main():
    print(titulos['lumiere'])
    print("""
0. Sair
1. Login
2. Cadastro
3. Editar | Excluir Conta
""")
    escolha = input("Escolha: ")
    match escolha:
        case "0":
            conn.close()
            finaliza_programa()
        case "1":
            login()
        case "2":
            ...
        case "3":
            ...
if __name__ == '__main__':
    main()