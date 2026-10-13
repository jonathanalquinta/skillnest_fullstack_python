import os
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

class MySQLConnection:
    def __init__(self, db=None):
        # Toma la base de datos pasada por el modelo o la definida en el .env
        database = db if db else os.getenv('DB_NAME', 'cinepedia_db')
        
        self.connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'root'),
            db=database,
            port=int(os.getenv('DB_PORT', 3306)),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    return cursor.fetchall()
                else:
                    self.connection.commit()
            except Exception as e:
                print("Error en base de datos:", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db=None):
    return MySQLConnection(db)