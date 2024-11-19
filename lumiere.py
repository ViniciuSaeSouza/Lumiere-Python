# 558843 - Laura de Oliveira Cintra - 1TDSPK
# 558832 - Maria Eduarda Alves da Paixão - 1TDSPK
# 554456 - Vinícius Saes de Souza - 1TDSPK
# import pandas as pd
from datetime import datetime
import os
import re
import oracledb
import random
from cria_conexao import recupera_conexao
from obter_pdf import obter_pdf_source


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
usuario_info = {
    'id' : 0,
    'nome' : '',
    'email' : '',
    'senha' : ''
}
# Funçõs e Rotinas

def limpa_tela():
    os.system('cls' if os.name == 'Nt' else 'clear')

def finalizar_programa():
    if conn != None:
        conn.close()
    limpa_tela()
    print("Obrigado por usar o Lumiere! \nFinalizando o programa....")
    exit()

def msg_opcao_invalida():
    print("---------------------------------------")
    print("Erro! Opção inválida, digite novamente.")

# Tenta recuperar uma conexao com o banco de dados da classe `cria_conexao`, se conseguir, cria um cursor para executar instruções SQL, se não, limpa o terminal de acordo com o sistema operacional
try:
    conn = recupera_conexao()
    if conn == None:
        raise Exception
    else:
        inst_sql = conn.cursor()
except Exception as e:
    limpa_tela()
    print(f"\t***ERRO*** \n- Ops! infelizmente tivemos uma falha ao recuperar a conexao com o banco de dados!\n- Verifique a conexão com o Banco de Dados Oracle no arquivo `cria_conexao` ou acione o autor do código! \n- Sentimos muito por isso! :(")
    input("Pressione qualquer tecla para sair do programa: ")
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
    
def obter_nome(contexto=str) -> str:
    while True:
        print("[S]air a qualquer momento")
        validacao, nome = valida_formato("nome", input("Nome: ").capitalize())
        if nome.upper() == "S":
            main()
            break
        elif contexto == "editar" and nome == '':
            return nome
        elif validacao:
            return nome
        else:
            print("---------------------------------------------------------------------------------")
            print("Erro! Nome não pode estar vazio nem conter caracteres especiais como ex.(@,*,&,%)\n")

def obter_email(contexto=str) -> str | dict:
    while True:
        print("[S]air a qualquer momento")
        validacao, email = valida_formato("email", input("E-mail: ").lower())
        if email.upper() == "S":
            main()
            break
        elif contexto == "editar" and email == '':
            return email
        elif validacao:
            data = busca_email_existente(email)
            if contexto == "login" or contexto == "excluir":
                if data:
                    return data
                else:
                    return {}
            
            if contexto == "cadastro":
                if not data:
                    return email
                else:
                    print("------------------------------------------------------")
                    print("Erro! Já existe um usuário com este e-mail cadastrado!\n")
                    while True:
                        escolha = input("0.Sair \n1. Digitar outro e-mail \n2. Fazer login \n3. Esqueci minha senha \nEscolha: ")
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


def obter_senha(contexto=str) -> str:
    while True:
        print("[S]air a qualquer momento")
        senha = input("Senha (sem padrão): ")
        if senha.upper() == "S":
            main()
            break
        elif contexto == "editar" and senha == '':
            return senha
        elif senha:
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
    cadastro_info['email'] = obter_email(contexto="cadastro")
    
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
                            msg_opcao_invalida()
            case _:
                msg_opcao_invalida()
                
def login():
    limpa_tela()
    mostra_titulo("login")
    print()
    try:
        while True:
            data = obter_email(contexto="login")
            if data:
                usuario_info['id'] = data[0][0]
                usuario_info['nome'] = data[0][1]
                usuario_info['email'] = data[0][2]
                usuario_info['senha'] = data[0][3]
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
        
            
                
        while True:    
            senha = obter_senha()
            if senha == usuario_info['senha']:
                menu_usuario()
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
    excluir_info = usuario_info.copy()
    limpa_tela()
    while True:
        mostra_titulo("editar | excluir conta")
        data = obter_email("excluir")
        if not data:
            print("-----------------------------------------")
            print("Erro! E-mail incorreto ou não cadastrado.")
        else: 
            excluir_info['nome'] = data[0][1]
            excluir_info['email'] = data[0][2]
            excluir_info['senha'] = data[0][3]
            while True:
                print("----------------------")
                escolha = input("0. Menu Inicial \n1. Excluir conta \n2. Editar Conta \nEscolha: ")
                match escolha:
                    case "0":
                        main()
                        break
                    case "1":
                        excluir_conta()
                        break
                    case "2":
                        editar_conta(excluir_info)
                        break
                    case _:
                        msg_opcao_invalida()
                    
def excluir_conta(excluir_info:dict):
    limpa_tela()
    mostra_titulo("excluir conta")
    while True:
        senha = input(f"""
Nome: {excluir_info['nome']}
E-mail: {excluir_info['email']}
Para confirmar a exclusão da conta, digite sua senha (Ao digitar a senha correta a conta será excluida)
Senha: """)
        
        if senha == excluir_info['senha']:
            sql = "DELETE FROM TBL_USUARIOS_PY WHERE email = :email"
            inst_sql.execute(sql, {'email' : excluir_info['email']})
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
    editar_info = {
        'nome' : '',
        'email' : '',
        'senha' : '',
    }
    limpa_tela()
    
    mostra_titulo("editar conta")
    
    print(f"""
Nome: {usuario_info['nome']}
E-mail: {usuario_info['email']}
Senha: {usuario_info['senha']}
Caso não deseje editar algo, deixe o campo vazio e aperte Enter""")
    
    nome = obter_nome(contexto="editar")
    email = obter_email(contexto="editar")
    senha = obter_senha(contexto="editar")

    editar_info['nome'] = nome if nome else usuario_info['nome']
    editar_info['email'] = email if email else usuario_info['email']
    editar_info['senha'] = senha if senha else usuario_info['senha']
    while True:
        print(f"""
Nome: {editar_info['nome']}
E-mail: {editar_info['email']}
Senha: {editar_info['senha']}
Confirmar alteração dos dados?""")
        escolha = input("1. Sim \n2. Não \n3. Menu \nEscolha: ")
        match escolha:
            case "1":
                sql = "UPDATE tbl_usuarios_py SET nome = :nome, email = :email, senha = :senha WHERE email = :email_atual"
                try:
                    inst_sql.execute(sql, {'nome' : editar_info['nome'], 'email' : editar_info['email'], 'senha' : editar_info['senha'], 'email_atual' : usuario_info['email']})
                    conn.commit()
                    print("Informações da conta atualizadas com sucesso!")
                    input("Aperte qualquer tecla para voltar ao menu principal: ")
                    main()
                    break
                except Exception as e:
                    print(f"Erro ao atualizar dados da base! Erro: {e}")
            case "2":
                editar_conta(usuario_info)
                break
            case "3":
                main()
                break
            case _:
                msg_opcao_invalida()

def menu_usuario():
    limpa_tela()
    mostra_titulo(f"Bem vindo(a), {usuario_info['nome']}")
    while True:
        escolha = input(
"""0. Sair
1. Registrar consumo
2. Gerar relatório
3. Fazer consulta
Escolha: """)
        
        match escolha:
            case "0":
                finalizar_programa()
            case "1":
                menu_registro_consumo()
            case "2":
                gerar_relatorio()
            case "3":
                ...
            case _:
                msg_opcao_invalida()
    
def menu_registro_consumo():
    while True:
        limpa_tela()
        mostra_titulo("registro de consumo")
        escolha = input("""**Recomendamos no ínicio cadastrar pelo menos 03 meses de consumo para que o gráfico possa ser gerado!**
0. Sair
1. Registro manual
2. Registrar via conta de luz
3. Simular registros
Escolha: """)
        match escolha:
            case "0":
                finalizar_programa()
            case "1":
                registro_manual()
            case "2":
                registro_pdf()
            case "3":
                simular_registros()

def registro_manual():
    limpa_tela()
    mostra_titulo("registro manual")
    
    # Funções auxiliares
    def obter_mes_consumo() -> int:
        while True:
            try:
                mes_consumo = int(input("Digite o número do mês de consumo ex.(Janeiro = 1): "))
                if mes_consumo < 1 or mes_consumo > 12:
                    print(f"Erro! Número do mês inválido: {mes_consumo}. Digite novamente.\n")
                else:
                    return mes_consumo
            except ValueError as e:
                print("Erro! Mês precisa ser um número.")
            except Exception as e:
                print(f"Erro ao salvar o mês consumo. Erro: {e}")
    def obter_consumo_kwh() -> int:
        while True:
            try:
                consumo_kwh = int(input("Digite o valor do consumo do respectivo mês ex.(kWh = 402): "))
                if consumo_kwh < 1:
                    print(f"Erro! Consumo não pode ser abaixo de 1. Digite novamente.\n")
                else:
                    return consumo_kwh
            except ValueError as e:
                print("Erro! Consumo kWh/mês precisa ser um número.")
            except Exception as e:
                print(f"Erro ao salvar o consumo kWh/mês. Erro: {e}")
   
    mes_consumo = obter_mes_consumo()
    consumo_kwh = obter_consumo_kwh()
    
    id = usuario_info['id']
    
    if cadastrar_consumo(mes_consumo, consumo_kwh, id):
        print("Cadastro do consumo realizado!")
        while True:
            escolha = input("Cadastrar outro mês? \n1.Sim \n2.Não(Menu usuario) \nEscolha: ")
            match escolha:
                case "1":
                    menu_registro_consumo()
                case "2":
                    menu_usuario()
                case _:
                    msg_opcao_invalida()

def registro_pdf():
    consumo_info = obter_pdf_source()
    while True:
        escolha = input("Deseja confirmar o cadastro do consumo? \n1. Sim \n2. Não(Menu registro) \nEscolha: ")
        match escolha:
            case "1":
                if cadastrar_consumo(consumo_info['mes_consumo'], consumo_info['consumo'], usuario_info['id']):
                    input("Resultado cadastrado com sucesso! \nAperte qualquer tecla para continuar: ")
                else:
                    input("Falha ao cadastrar o consumo! Verifique se o mês da conta já não foi cadastrado \nAperte qualquer tecla para continuar: ")
                break
            case "2":
                menu_registro_consumo()
                break
            case _:
                msg_opcao_invalida()
        


def simular_registros():
    limpa_tela()
    mostra_titulo("Simular Registros de Consumo")
    # Solicitar ao usuário o número de registros a serem simulados
    while True:
        try:
            num_registros = int(input("Quantos registros você deseja simular? \nEscolha: "))
            if num_registros < 1:
                print("Erro! O número de registros deve ser pelo menos 1.")
            else:
                break
        except ValueError:
            print("Erro! Por favor, insira um número válido.")
    
    id_usuario = usuario_info['id']
    ano_atual = datetime.now().year  # Obtendo o ano atual
   # Começar do mês atual
    mes_atual = datetime.now().month
    
    for i in range(num_registros):
        # Calcular o mês e o ano para cada registro
        mes_consumo = mes_atual - i
        ano_consumo = ano_atual + (mes_consumo - 1) // 12  # Incrementa o ano se necessário
        mes_consumo = (mes_consumo - 1) % 12 + 1 
        # Formatar o mês e ano no formato "MM-YYYY"
        mes_ano_consumo = f"{mes_consumo:02d}-{ano_consumo}"
        # Gerar um consumo aleatório entre 150 e 1000 kWh
        consumo_kwh = random.randint(150, 1000)
        
        # Cadastrar o consumo gerado no banco de dados
        if cadastrar_consumo(mes_ano_consumo, consumo_kwh, id_usuario):
            print(f"Registro cadastrado: Mês {mes_ano_consumo}, Consumo {consumo_kwh} kWh.")
        else:
            print(f"Falha ao cadastrar o registro para o mês {mes_ano_consumo}.")
    
    input("Simulação concluída! Aperte qualquer tecla para voltar ao menu de registro de consumo: ")
    menu_registro_consumo()

    
    
   

def cadastrar_consumo(mes_consumo:str|int, consumo_kwh:int, id:int) -> bool:
    try:
        sql = "INSERT INTO tbl_consumos_py (id_usuario, consumo, mes_consumo) VALUES (:id, :consumo, TO_DATE(:mes_consumo, 'MM-YYYY'))"
        inst_sql.execute(sql, {'id' : id, 'consumo' : consumo_kwh, 'mes_consumo' : mes_consumo})
        conn.commit()
        return True
    except oracledb.DatabaseError:
        return False
    except Exception as e:
        print(f"Falha ao cadastrar consumo na base de dados! Erro: {e}")
        return False
    

def gerar_relatorio():
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
                msg_opcao_invalida()

if __name__ == '__main__':
    main()