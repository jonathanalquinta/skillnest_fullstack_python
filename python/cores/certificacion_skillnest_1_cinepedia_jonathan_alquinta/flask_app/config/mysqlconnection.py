import os
import pymysql.cursors
from dotenv import load_dotenv

# variables de entorno
load_dotenv()

# clasee de conexion en mysql
class MySQLConnection:
    def __init__(self, db=None):
        # Toma la base de datos pasada por parámetro o la definida en el .env
        database = db if db else os.environ.get('MYSQL_DATABASE', os.environ.get('DB_NAME', 'cinepedia_db'))

        connection = pymysql.connect(
            host=os.environ.get('MYSQL_HOST', os.environ.get('DB_HOST', 'localhost')),
            user=os.environ.get('MYSQL_USER', os.environ.get('DB_USER', 'root')),
            password=os.environ.get('MYSQL_PASSWORD', os.environ.get('DB_PASSWORD', 'root')),
            db=database,
            port=int(os.environ.get('MYSQL_PORT', os.environ.get('DB_PORT', 3306))),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.connection = connection

    # metodo para hacer consultas
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print(f"Ejecutando Consulta: {query}")
                cursor.execute(query)
                
                query_str = query if isinstance(query, str) else query.decode('utf-8')

                if query_str.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query_str.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
                    return True
            except Exception as e:
                print(f"Error en la Base de Datos: {e}")
                return False
            finally:
                self.connection.close()

# INSTANCIACIÓN (Soporta ambos nombres para importación)
def connectToMySQL(db=None):
    return MySQLConnection(db)

connect_to_mysql = connectToMySQL