import re
from datetime import datetime, date
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOMBRE_REGEX = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$')
# Bonus Plata: Mínimo 8 caracteres, al menos 1 letra mayúscula y 1 número
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d).{8,}$')

class Usuario:
    DB = "esquema_registro_login"

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.fecha_nacimiento = data['fecha_nacimiento']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password, fecha_nacimiento)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, %(fecha_nacimiento)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        data = {'email': email}
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result or len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        data = {'id': user_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result or len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validar_registro(usuario):
        is_valid = True

        # Validar Nombre
        if len(usuario.get('nombre', '').strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            is_valid = False
        elif not NOMBRE_REGEX.match(usuario.get('nombre', '')):
            flash("El nombre solo debe contener letras.", "registro")
            is_valid = False

        # Validar Apellido
        if len(usuario.get('apellido', '').strip()) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            is_valid = False
        elif not NOMBRE_REGEX.match(usuario.get('apellido', '')):
            flash("El apellido solo debe contener letras.", "registro")
            is_valid = False

        # Validar Email
        if not EMAIL_REGEX.match(usuario.get('email', '')):
            flash("Dirección de e-mail inválida.", "registro")
            is_valid = False
        else:
            usuario_existente = Usuario.get_by_email(usuario['email'])
            if usuario_existente:
                flash("El correo electrónico ya está registrado.", "registro")
                is_valid = False

        # Bonus Oro: Validar Fecha de Nacimiento / Mayoría de edad
        if not usuario.get('fecha_nacimiento'):
            flash("Debes ingresar tu fecha de nacimiento.", "registro")
            is_valid = False
        else:
            try:
                fecha_nac = datetime.strptime(usuario['fecha_nacimiento'], '%Y-%m-%d').date()
                hoy = date.today()
                edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
                if edad < 18:
                    flash("Debes tener al menos 18 años para registrarte.", "registro")
                    is_valid = False
            except ValueError:
                flash("Formato de fecha inválido.", "registro")
                is_valid = False

        # Bonus Plata: Validar Contraseña (mínimo 8 caracteres, 1 mayúscula, 1 número)
        if not PASSWORD_REGEX.match(usuario.get('password', '')):
            flash("La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula y un número.", "registro")
            is_valid = False

        # Confirmación de contraseña
        if usuario.get('password') != usuario.get('confirm_password'):
            flash("Las contraseñas no coinciden.", "registro")
            is_valid = False

        return is_valid