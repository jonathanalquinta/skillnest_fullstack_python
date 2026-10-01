import re
from flask import flash
from app.config.conexion_bd import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    def __init__(self, datos):
        self.id = datos['id']
        self.nombre = datos['nombre']
        self.apellido = datos['apellido']
        self.email = datos['email']
        self.contrasena = datos['contrasena']
        self.creado_en = datos['creado_en']
        self.actualizado_en = datos['actualizado_en']

    @classmethod
    def guardar(cls, datos):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, contrasena)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(contrasena)s);
        """
        return connectToMySQL().ejecutar_consulta(query, datos)

    @classmethod
    def obtener_por_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL().ejecutar_consulta(query, {'email': email})
        if len(resultado) < 1:
            return False
        return cls(resultado[0])

    @classmethod
    def obtener_por_id(cls, usuario_id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultado = connectToMySQL().ejecutar_consulta(query, {'id': usuario_id})
        if len(resultado) < 1:
            return False
        return cls(resultado[0])

    @staticmethod
    def validar_registro(formulario):
        es_valido = True

        if len(formulario['nombre'].strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            es_valido = False

        if len(formulario['apellido'].strip()) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            es_valido = False

        if not EMAIL_REGEX.match(formulario['email']):
            flash("El correo electrónico no tiene un formato válido.", "registro")
            es_valido = False
        elif Usuario.obtener_por_email(formulario['email']):
            flash("El correo electrónico ya se encuentra registrado.", "registro")
            es_valido = False

        if len(formulario['contrasena']) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "registro")
            es_valido = False

        if formulario['contrasena'] != formulario['confirmar_contrasena']:
            flash("Las contraseñas no coinciden.", "registro")
            es_valido = False

        return es_valido