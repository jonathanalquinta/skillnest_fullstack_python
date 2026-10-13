from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

DB = 'cinepedia_db'

class Pelicula:
    def __init__(self, data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.director = data['director']
        self.fecha_estreno = data['fecha_estreno']
        self.sinopsis = data['sinopsis']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creador_nombre = data.get('creador_nombre', '')

    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO peliculas (titulo, director, fecha_estreno, sinopsis, usuario_id)
            VALUES (%(titulo)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(usuario_id)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def obtener_todas(cls):
        query = """
            SELECT peliculas.*, usuarios.nombre AS creador_nombre 
            FROM peliculas 
            JOIN usuarios ON peliculas.usuario_id = usuarios.id
            ORDER BY peliculas.id DESC;
        """
        results = connectToMySQL(DB).query_db(query)
        peliculas = []
        if results:
            for row in results:
                peliculas.append(cls(row))
        return peliculas

    @classmethod
    def obtener_por_id(cls, pelicula_id):
        data = {'id': pelicula_id}
        query = """
            SELECT peliculas.*, usuarios.nombre AS creador_nombre 
            FROM peliculas 
            JOIN usuarios ON peliculas.usuario_id = usuarios.id 
            WHERE peliculas.id = %(id)s;
        """
        result = connectToMySQL(DB).query_db(query, data)
        if not result or len(result) == 0:
            return None
        return cls(result[0])

    @classmethod
    def obtener_por_titulo(cls, titulo):
        data = {'titulo': titulo.strip()}
        query = "SELECT * FROM peliculas WHERE LOWER(titulo) = LOWER(%(titulo)s);"
        result = connectToMySQL(DB).query_db(query, data)
        if not result or len(result) < 1:
            return None
        return cls(result[0])

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE peliculas 
            SET titulo = %(titulo)s, director = %(director)s, 
                fecha_estreno = %(fecha_estreno)s, sinopsis = %(sinopsis)s 
            WHERE id = %(id)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def eliminar(cls, pelicula_id):
        data = {'id': pelicula_id}
        query = "DELETE FROM peliculas WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)

    @staticmethod
    def validar_pelicula(form_data, pelicula_id=None):
        is_valid = True

        titulo = form_data.get('titulo', '').strip()
        director = form_data.get('director', '').strip()
        fecha_estreno = form_data.get('fecha_estreno', '').strip()
        sinopsis = form_data.get('sinopsis', '').strip()

        # Todos los campos obligatorios y mínimo 3 caracteres[cite: 2, 3]
        if len(titulo) < 3:
            flash("El nombre de la película debe tener al menos 3 caracteres.", "error")
            is_valid = False

        if len(director) < 3:
            flash("El director debe tener al menos 3 caracteres.", "error")
            is_valid = False

        if not fecha_estreno or len(fecha_estreno) < 3:
            flash("La fecha de estreno no puede estar vacía.", "error")
            is_valid = False

        if len(sinopsis) < 3:
            flash("Sinopsis no puede estar vacía", "error")
            is_valid = False

        # El nombre debe ser único, pero puede ser el mismo al editar[cite: 2, 3]
        pelicula_existente = Pelicula.obtener_por_titulo(titulo)
        if pelicula_existente:
            if pelicula_id is None or pelicula_existente.id != int(pelicula_id):
                flash("El nombre de la película ya existe.", "error")
                is_valid = False

        return is_valid