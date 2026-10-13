from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/cine')
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')
    
    usuario_id = Usuario.guardar(request.form)
    session['usuario_id'] = usuario_id
    session['usuario_nombre'] = request.form['nombre'].strip()
    return redirect('/cine')

@app.route('/login', methods=['POST'])
def login():
    usuario = Usuario.validar_login(request.form)
    if not usuario:
        return redirect('/')
    
    session['usuario_id'] = usuario.id
    session['usuario_nombre'] = usuario.nombre
    return redirect('/cine')

@app.route('/logout')
def logout():
    # Borra la sesión y redirige al Login[cite: 1]
    session.clear()
    return redirect('/')