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

def finalizar_programa():
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
    finalizar_programa()
    


# Recebe um texto:titulo como parâmetro e mostra no terminal
def mostra_titulo(titulo:str):
    tam = len(titulo)
    print("**" * (tam + 2))
    print(f"{" " * (tam // 2)}--{titulo.upper()}--")
    print("**" * (tam + 2))


def valida_formato(padrao:str, texto:str) -> tuple[bool,str]:
    texto = texto.lower()
    if re.match(padroes_re[padrao], texto):
        return (True, texto)
    else:
        return (False, texto)
    
def obter_nome() -> str:
    while True:
        confirmacao, nome = valida_formato("nome", input("Nome: ").capitalize())
        if confirmacao:
            return nome
        else:
            print("---------------------------------------------------------------------------------")
            print("Erro! Nome não pode estar vazio nem conter caracteres especiais como ex.(@,*,&,%)\n")


def obter_email() -> str:
    while True:
        confirmacao, email = valida_formato("email", input("E-mail: ").lower())
        if confirmacao:
            data = busca_email_existente(email)
            if not data:
                return email
            else:
                print("------------------------------------------------------")
                print("Erro! Já existe um usuário com este e-mail cadastrado!\n")
                while True:
                    escolha = input("0.Sair \n1. Digitar outro e-mail \n2.Fazer login \n3. Esqueci minha senha \nEscolha: ")
                    match escolha:
                        case "0":
                            finalizar_programa()
                        case "1":
                            break
                        case "2":
                            login()
                            break
                        case "3":
                            editar_excluir_conta()
                            break
                        case _:
                            print("--------------------------------------")
                            print("Erro! Opção inválida, digite novamente")       
        else:
            print("------------------------------------------------------------------------")
            print("Erro! Formato de E-mail inválido. Exemplo válido: exemplo@dominio.com.br \n")


def obter_senha() -> str:
    while True:
        senha = input("Senha (sem padrão): ")
        if senha:
            return senha
        else:
            print("--------------------------------")
            print("Erro! Senha não pode estar vazia")


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
    limpa_tela()
    mostra_titulo("cadastro")
    cadastro_info = {
        'nome' : '',
        'email' : '',
        'senha': '',
    }
    
    # Nome
    cadastro_info['nome'] = obter_nome()
    
    # E - mail
    cadastro_info['email'] = obter_email()
    
    # Senha
    cadastro_info['senha'] = obter_senha()
    
    while True:
        limpa_tela()
        print(f"""
Nome: {cadastro_info['nome']}
E-mail: {cadastro_info['email']}
Senha: {cadastro_info['senha']}
Confirmar cadastro?
    """)
        escolha = input("[S]im || [N]ão: ").upper()
        limpa_tela()
        match escolha:
            case "S":
                try:
                    sql = "INSERT INTO tbl_usuarios_py (nome, email, senha) VALUES (:nome, :email, :senha)"
                    inst_sql.execute(sql, (cadastro_info["nome"], cadastro_info["email"], cadastro_info["senha"]))
                    conn.commit()
                    input("Cadastro realizado com sucesso! \nAperte qualquer tecla para ser redirecionado à tela de login: ")
                    login()
                    break
                except Exception as e:
                    print("---------------------------------------------------------")
                    print(f"Falha ao realizar o cadastro na base de dados! Erro: {e}")
                    break
            case "N":
                while True:
                    escolha = input("0. Sair \n1. Preencher cadastro novamente \nEscolha: ")
                    match escolha:
                        case "0":
                            finalizar_programa()
                        case "1":
                            cadastro()
                            break
                        case _ :
                            print("Erro! Opção inválida, digite novamente.")
            case _:
                print("Erro! Opção inválida, digite novamente.")
                

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
            confirmacao, email = valida_formato("email", input("E-mail: ").lower())
            if confirmacao:
                data = busca_email_existente(email)
                if data:
                    login_info['nome'] = data[0][1]
                    login_info['email'] = data[0][2]
                    login_info['senha'] = data[0][3]
                    break
                else:
                    print("---------------------")                
                    print("E-mail incorreto ou ainda não cadastrado!\n")
                    escolha = input("1. Digitar novamente \n2. Fazer Cadastro \nEscolha: ")
                    match escolha:
                        case "1":
                            pass
                        case "2":
                            cadastro()
                            break
                        case _:
                            print("Opção inválida! Digite novamente: ")
                            escolha = input("1. Digitar novamente \n2. Fazer Cadastro \nEscolha: ")
            else:
                print("Erro! Formato de E-mail inválido. Exemplo válido: exemplo@dominio.com.br \n")
                
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
    limpa_tela()
    while True:
        mostra_titulo("editar | excluir conta")
        usuario_info = {
            'nome' : '',
            'email' : '',
            'senha' : '',
        }
        confirmacao, email = valida_formato("email", input("E-mail | [S]air: ").lower())
        if email == 's':
            main()
            break
        elif not confirmacao:
            print("------------------------------------------------------------------------")
            print("Erro! Formato de E-mail inválido. Exemplo válido: exemplo@dominio.com.br\n")
        else:
            data = busca_email_existente(email)
            if not data:
                print("-----------------------------------------")
                print("Erro! E-mail incorreto ou não cadastrado.")
            else: 
                usuario_info['nome'] = data[0][1]
                usuario_info['email'] = data[0][2]
                usuario_info['senha'] = data[0][3]
                while True:
                    print("----------------------")
                    escolha = input("0.Menu Inicial \n1. Excluir conta \n2.Editar Conta \nEscolha: ")
                    match escolha:
                        case "0":
                            main()
                            break
                        case "1":
                            excluir_conta(usuario_info)
                            break
                        case "2":
                            editar_conta(usuario_info)
                            break
                        case _:
                            print("---------------------------------------")
                            print("Erro! Opção inválida, digite novamente.")
                    
def excluir_conta(usuario_info:dict):
    limpa_tela()
    mostra_titulo("excluir conta")
    while True:
        senha = input(f"""
Nome: {usuario_info['nome']}
E-mail: {usuario_info['email']}
Para confirmar a exclusão da conta, digite sua senha (Ao digitar a senha correta a conta será excluida)
Senha: """)
        
        if senha == usuario_info['senha']:
            sql = "DELETE FROM TBL_USUARIOS_PY WHERE email = :email"
            inst_sql.execute(sql, (usuario_info['email'],))
            conn.commit()
            input("Usuário deletado com sucesso! \nAperte qualquer tecla para voltar ao menu inicial: ")
            main()
            break
        else:
            print("Senha incorreta! \n Digitar novamente? ")
            escolha = input("1. Sim \n2. Menu \nEscolha: ")
            match escolha:
                case "1":
                    pass
                case "2":
                    main()
                    break
                

def editar_conta():
    pass
    

def dashboard(info:dict):
    pass

def main():
    limpa_tela()
    mostra_titulo("lumiere")
    while True:
        escolha = input("""
0. Sair
1. Login
2. Cadastro
3. Editar | Excluir Conta
Escolha: """)
        match escolha:
            case "0":
                conn.close()
                finalizar_programa()
            case "1":
                login()
                break
            case "2":
                cadastro()
                break
            case "3":
                editar_excluir_conta()
                break
            case _:
                print("---------------------------------------")
                print("Erro! Opção inválida, digite novamente.")

if __name__ == '__main__':
    main()