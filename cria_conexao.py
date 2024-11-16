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
	