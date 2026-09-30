from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password": pw_hash,
        "fecha_nacimiento": request.form['fecha_nacimiento']
    }

    user_id = Usuario.save(data)
    session['usuario_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    usuario = Usuario.get_by_email(request.form['email'])
    if not usuario:
        flash("Credenciales inválidas (correo no encontrado).", "login")
        return redirect('/')

    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Credenciales inválidas (contraseña incorrecta).", "login")
        return redirect('/')

    session['usuario_id'] = usuario.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')

    usuario = Usuario.get_by_id(session['usuario_id'])
    if not usuario:
        session.clear()
        return redirect('/')

    return render_template('dashboard.html', usuario=usuario)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')