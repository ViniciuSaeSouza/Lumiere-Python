import oracledb
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("user")
password = os.getenv("password")
dsn = os.getenv("dsn")

def recupera_conexao() -> oracledb.Connection:
    
	try:
		conn = oracledb.connect(user=user, password=password, dsn=dsn)
		return conn
	except oracledb.OperationalError as e:
		print("Falha ao criar conexão!")
	
	# else:
	#     conexao = True
	#     ano_mes_dia = str(datetime.now().date())
	#     ano_mes_dia = ano_mes_dia.replace("-", "")
	#     hora = str(datetime.now().hour) + (str)(datetime.now().minute) + (str)(datetime.now().second)
	#     dia_hora = ano_mes_dia + hora
 