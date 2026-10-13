from flask_app.config.mysqlconnection import connectToMySQL

DB = 'cinepedia_db'

class Comentario:
    def __init__(self, data):
        self.id = data['id']
        self.contenido = data['contenido']
        self.usuario_id = data['usuario_id']
        self.pelicula_id = data['pelicula_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuario_nombre = data.get('usuario_nombre', '')

    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO comentarios (contenido, usuario_id, pelicula_id)
            VALUES (%(contenido)s, %(usuario_id)s, %(pelicula_id)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def obtener_por_pelicula(cls, pelicula_id):
        data = {'pelicula_id': pelicula_id}
        query = """
            SELECT comentarios.*, usuarios.nombre AS usuario_nombre 
            FROM comentarios 
            JOIN usuarios ON comentarios.usuario_id = usuarios.id 
            WHERE pelicula_id = %(pelicula_id)s 
            ORDER BY comentarios.created_at DESC;
        """
        results = connectToMySQL(DB).query_db(query, data)
        comentarios = []
        if results:
            for row in results:
                comentarios.append(cls(row))
        return comentarios

    @classmethod
    def obtener_por_id(cls, comentario_id):
        data = {'id': comentario_id}
        query = "SELECT * FROM comentarios WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        if not result or len(result) == 0:
            return None
        return cls(result[0])

    @classmethod
    def eliminar(cls, comentario_id):
        data = {'id': comentario_id}
        query = "DELETE FROM comentarios WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)