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
    print("**" * (tam + 2))
    print(f"{" " * (tam // 2)}--{titulo.upper()}--")
    print("**" * (tam + 2))


def valida_formato(padrao:str, texto:str) -> bool:
    if re.match(padroes_re[padrao], texto):
        return True
    else:
        return False
    
def busca_email_existente(email:str) -> list:
    try:
        sql = f"SELECT * FROM tbl_usuarios_py WHERE email = :email"
        inst_sql.execute(sql, (email,))
        data = inst_sql.fetchall()
        return data if data else []
    except Exception as e:
        print(f"Falha ao buscar e-mail na base de dados! ERRO: {e}")
        return []
        
        
        
def cadastro():
    pass


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
            email = input("E-mail: ").lower()
            if valida_formato("email", email):
                data = busca_email_existente(email)
                if data:
                    login_info['nome'] = data[0][1]
                    login_info['email'] = data[0][2]
                    login_info['senha'] = data[0][3]
                    break
                else:
                    print("---------------------")                
                    print("E-mail incorreto ou ainda não cadastrado!")
                    escolha = input("1. Digitar novamente \n2. Fazer Cadastro \nEscolha: ")
                    match escolha:
                        case "1":
                            pass
                        case "2":
                            cadastro()
                        case _:
                            print("Opção inválida! Digite novamente: ")
                            escolha = input("1. Digitar novamente \n2. Fazer Cadastro \nEscolha: ")
            else:
                print("Formato do email inválido!")
                
        while True:    
            senha = input("Senha: ")
            if senha == login_info['senha']:
                dashboard(login_info)
                break
            else:
                print("---------------------")
                print("Senha incorreta!")
                while True:
                    escolha = input("1. Digitar novamente \n2. Esqueci minha senha \nEscolha: ")
                    match escolha:
                        case "1":
                            break
                        case "2":
                            editar_excluir_conta()
                            break
                        case _:
                            print("---------------------")
                            print("Opção inválida")
            
    except Exception as e:
        print(f"ERRO: {e}")

def editar_excluir_conta():
    pass

def dashboard(info:dict):
    pass

def main():
    limpa_tela()
    mostra_titulo("lumiere")
    escolha = input("""
0. Sair
1. Login
2. Cadastro
3. Editar | Excluir Conta
Escolha: 
""")
    match escolha:
        case "0":
            conn.close()
            finaliza_programa()
        case "1":
            login()
        case "2":
            pass
        case "3":
            pass

if __name__ == '__main__':
    main()