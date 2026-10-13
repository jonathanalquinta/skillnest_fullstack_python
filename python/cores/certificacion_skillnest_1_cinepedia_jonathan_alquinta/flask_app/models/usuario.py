import re
from flask import flash
from flask_app import bcrypt
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DB = 'cinepedia_db'

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def guardar(cls, form_data):
        pw_hash = bcrypt.generate_password_hash(form_data['password'])
        data = {
            'nombre': form_data['nombre'].strip(),
            'apellido': form_data['apellido'].strip(),
            'email': form_data['email'].strip().lower(),
            'password': pw_hash
        }
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def obtener_por_email(cls, email):
        data = {'email': email.strip().lower()}
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query, data)
        if not result or len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validar_registro(form_data):
        is_valid = True

        nombre = form_data.get('nombre', '').strip()
        apellido = form_data.get('apellido', '').strip()
        email = form_data.get('email', '').strip()
        password = form_data.get('password', '')
        confirm_password = form_data.get('confirm_password', '')

        # Nombre y apellido deben tener al menos 2 caracteres[cite: 1]
        if len(nombre) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            is_valid = False

        if len(apellido) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            is_valid = False

        # Formato de email válido[cite: 1]
        if not EMAIL_REGEX.match(email):
            flash("El formato del correo electrónico no es válido.", "registro")
            is_valid = False

        # Email no repetido en la BD[cite: 1]
        if Usuario.obtener_por_email(email):
            flash("El correo electrónico ya se encuentra registrado.", "registro")
            is_valid = False

        # Contraseña y confirmación iguales[cite: 1]
        if len(password) < 1 or password != confirm_password:
            flash("Las contraseñas no coinciden.", "registro")
            is_valid = False

        return is_valid

    @staticmethod
    def validar_login(form_data):
        email = form_data.get('email', '').strip()
        password = form_data.get('password', '')

        # Email registrado en BD[cite: 1]
        usuario = Usuario.obtener_por_email(email)
        if not usuario:
            flash("Credenciales inválidas.", "login")
            return False

        # Contraseña correspondiente[cite: 1]
        if not bcrypt.check_password_hash(usuario.password, password):
            flash("Credenciales inválidas.", "login")
            return False

        return usuario