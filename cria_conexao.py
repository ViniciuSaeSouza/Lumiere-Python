import oracledb
def recupera_conexao() -> oracledb.Connection:
	try:
		conn = oracledb.connect(user="RM554456", password="080995", dsn="oracle.fiap.com.br:1521/ORCL")
		return conn
	except oracledb.OperationalError as e:
		print("Falha ao criar conexão!")
	
	# else:
	#     conexao = True
	#     ano_mes_dia = str(datetime.now().date())
	#     ano_mes_dia = ano_mes_dia.replace("-", "")
	#     hora = str(datetime.now().hour) + (str)(datetime.now().minute) + (str)(datetime.now().second)
	#     dia_hora = ano_mes_dia + hora
 