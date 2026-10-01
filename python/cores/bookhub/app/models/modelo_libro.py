from datetime import datetime
from flask import flash
from app.config.conexion_bd import connectToMySQL

class Libro:
    def __init__(self, datos):
        self.id = datos['id']
        self.titulo = datos['titulo']
        self.autor = datos['autor']
        self.genero = datos['genero']
        self.fecha_publicacion = datos['fecha_publicacion']
        self.descripcion = datos['descripcion']
        self.usuario_id = datos['usuario_id']
        self.creado_en = datos['creado_en']
        self.actualizado_en = datos['actualizado_en']
        self.publicado_por = datos.get('publicado_por', '')
        self.total_favoritos = datos.get('total_favoritos', 0)

    @classmethod
    def guardar(cls, datos):
        query = """
            INSERT INTO libros (titulo, autor, genero, fecha_publicacion, descripcion, usuario_id)
            VALUES (%(titulo)s, %(autor)s, %(genero)s, %(fecha_publicacion)s, %(descripcion)s, %(usuario_id)s);
        """
        return connectToMySQL().ejecutar_consulta(query, datos)

    @classmethod
    def obtener_por_usuario(cls, usuario_id):
        query = """
            SELECT l.*, COUNT(f.usuario_id) AS total_favoritos
            FROM libros l
            LEFT JOIN favoritos f ON l.id = f.libro_id
            WHERE l.usuario_id = %(usuario_id)s
            GROUP BY l.id;
        """
        resultados = connectToMySQL().ejecutar_consulta(query, {'usuario_id': usuario_id})
        libros = []
        for fila in resultados:
            libros.append(cls(fila))
        return libros

    @classmethod
    def obtener_comunidad(cls, usuario_id):
        query = """
            SELECT l.*, CONCAT(u.nombre, ' ', u.apellido) AS publicado_por, COUNT(f.usuario_id) AS total_favoritos
            FROM libros l
            JOIN usuarios u ON l.usuario_id = u.id
            LEFT JOIN favoritos f ON l.id = f.libro_id
            WHERE l.usuario_id != %(usuario_id)s
            GROUP BY l.id;
        """
        resultados = connectToMySQL().ejecutar_consulta(query, {'usuario_id': usuario_id})
        libros = []
        for fila in resultados:
            libros.append(cls(fila))
        return libros

    @classmethod
    def obtener_por_id(cls, libro_id):
        query = """
            SELECT l.*, CONCAT(u.nombre, ' ', u.apellido) AS publicado_por, COUNT(f.usuario_id) AS total_favoritos
            FROM libros l
            JOIN usuarios u ON l.usuario_id = u.id
            LEFT JOIN favoritos f ON l.id = f.libro_id
            WHERE l.id = %(id)s
            GROUP BY l.id;
        """
        resultado = connectToMySQL().ejecutar_consulta(query, {'id': libro_id})
        if not resultado:
            return None
        return cls(resultado[0])

    @classmethod
    def actualizar(cls, datos):
        query = """
            UPDATE libros 
            SET titulo = %(titulo)s, autor = %(autor)s, genero = %(genero)s, 
                fecha_publicacion = %(fecha_publicacion)s, descripcion = %(descripcion)s
            WHERE id = %(id)s AND usuario_id = %(usuario_id)s;
        """
        return connectToMySQL().ejecutar_consulta(query, datos)

    @classmethod
    def eliminar(cls, libro_id, usuario_id):
        query = "DELETE FROM libros WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL().ejecutar_consulta(query, {'id': libro_id, 'usuario_id': usuario_id})

    @classmethod
    def agregar_favorito(cls, usuario_id, libro_id):
        query = "INSERT IGNORE INTO favoritos (usuario_id, libro_id) VALUES (%(usuario_id)s, %(libro_id)s);"
        return connectToMySQL().ejecutar_consulta(query, {'usuario_id': usuario_id, 'libro_id': libro_id})

    @classmethod
    def es_favorito(cls, usuario_id, libro_id):
        query = "SELECT * FROM favoritos WHERE usuario_id = %(usuario_id)s AND libro_id = %(libro_id)s;"
        resultado = connectToMySQL().ejecutar_consulta(query, {'usuario_id': usuario_id, 'libro_id': libro_id})
        return len(resultado) > 0

    @classmethod
    def obtener_favoritos_usuario(cls, usuario_id):
        query = """
            SELECT l.* FROM libros l
            JOIN favoritos f ON l.id = f.libro_id
            WHERE f.usuario_id = %(usuario_id)s;
        """
        resultados = connectToMySQL().ejecutar_consulta(query, {'usuario_id': usuario_id})
        return [cls(f) for f in resultados]

    @classmethod
    def obtener_usuarios_que_agregaron_favorito(cls, libro_id):
        query = """
            SELECT u.nombre, u.apellido FROM usuarios u
            JOIN favoritos f ON u.id = f.usuario_id
            WHERE f.libro_id = %(libro_id)s;
        """
        return connectToMySQL().ejecutar_consulta(query, {'libro_id': libro_id})

    @staticmethod
    def validar_libro(formulario):
        es_valido = True

        if not formulario.get('titulo') or len(formulario['titulo'].strip()) < 2:
            flash("El título debe tener al menos 2 caracteres.", "libro")
            es_valido = False

        if not formulario.get('autor') or len(formulario['autor'].strip()) < 2:
            flash("El autor es obligatorio.", "libro")
            es_valido = False

        if not formulario.get('genero'):
            flash("Debes seleccionar un género.", "libro")
            es_valido = False

        if not formulario.get('fecha_publicacion'):
            flash("La fecha de publicación es obligatoria.", "libro")
            es_valido = False
        else:
            fecha_ingresada = datetime.strptime(formulario['fecha_publicacion'], '%Y-%m-%d').date()
            if fecha_ingresada > datetime.now().date():
                flash("La fecha de publicación no puede ser futura.", "libro")
                es_valido = False

        if not formulario.get('descripcion') or len(formulario['descripcion'].strip()) < 10:
            flash("La descripción debe tener al menos 10 caracteres.", "libro")
            es_valido = False

        return es_valido