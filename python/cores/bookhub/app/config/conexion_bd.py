import pymysql.cursors

class ConectarBD:
    def __init__(self, bd='esquema_bookhub'):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'root'
        self.db = bd

    def ejecutar_consulta(self, query, data=None):
        conexion = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, data or ())
                if query.strip().upper().startswith("SELECT"):
                    resultado = cursor.fetchall()
                    return resultado
                else:
                    return cursor.lastrowid
        finally:
            conexion.close()

def connectToMySQL(bd='esquema_bookhub'):
    return ConectarBD(bd)