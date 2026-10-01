from flask import render_template, request, redirect, session, flash
from app import app, bcrypt
from app.models.modelo_usuario import Usuario

@app.route('/')
def inicio():
    if 'usuario_id' in session:
        return redirect('/libros')
    return render_template('inicio_registro.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    if not Usuario.validar_registro(request.form):
        return redirect('/')

    hash_password = bcrypt.generate_password_hash(request.form['contrasena']).decode('utf-8')
    
    datos = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'contrasena': hash_password
    }

    usuario_id = Usuario.guardar(datos)
    session['usuario_id'] = usuario_id
    session['nombre'] = datos['nombre']
    
    return redirect('/libros')

@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    usuario = Usuario.obtener_por_email(request.form['email'])
    if not usuario or not bcrypt.check_password_hash(usuario.contrasena, request.form['contrasena']):
        flash("Credenciales inválidas.", "login")
        return redirect('/')

    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre
    return redirect('/libros')

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    return redirect('/')