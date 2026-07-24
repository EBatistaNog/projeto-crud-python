import mysql.connector

def conectar():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '1234',    
        database = 'crud',
        port = 3306,
        use_pure=True
    )
    return conexao
