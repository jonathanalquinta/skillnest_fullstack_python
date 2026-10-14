from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario

@app.route('/cine')
def dashboard():
    # Requiere iniciar sesión
    if 'usuario_id' not in session:
        return redirect('/')
    
    peliculas = Pelicula.obtener_todas()
    return render_template('dashboard.html', peliculas=peliculas)

@app.route('/cine/nueva')
def nueva_pelicula():
    # Requiere iniciar sesión
    if 'usuario_id' not in session:
        return redirect('/')
    
    draft = session.pop('draft_nueva', None)
    return render_template('nueva_pelicula.html', draft=draft)

@app.route('/cine/crear', methods=['POST'])
def crear_pelicula():
    if 'usuario_id' not in session:
        return redirect('/')

    # Almacena la sinopsis y datos ingresados para preservarlos en caso de errores
    if not Pelicula.validar_pelicula(request.form):
        session['draft_nueva'] = request.form
        return redirect('/cine/nueva')

    datos = {
        'titulo': request.form['titulo'].strip(),
        'director': request.form['director'].strip(),
        'fecha_estreno': request.form['fecha_estreno'].strip(),
        'sinopsis': request.form['sinopsis'].strip(),
        'usuario_id': session['usuario_id']
    }
    Pelicula.guardar(datos)
    return redirect('/cine')

@app.route('/cine/<int:id>')
def ver_pelicula(id):
    # Requiere iniciar sesión
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula = Pelicula.obtener_por_id(id)
    if not pelicula:
        return redirect('/cine')

    comentarios = Comentario.obtener_por_pelicula(id)
    return render_template('ver_pelicula.html', pelicula=pelicula, comentarios=comentarios)

@app.route('/cine/editar/<int:id>')
def editar_pelicula(id):
    # Requiere iniciar sesión
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula = Pelicula.obtener_por_id(id)
    
    # Solamente el creador puede editar
    if not pelicula or pelicula.usuario_id != session['usuario_id']:
        return redirect('/cine')

    draft = session.pop('draft_editar', None)
    return render_template('editar_pelicula.html', pelicula=pelicula, draft=draft)

@app.route('/cine/actualizar/<int:id>', methods=['POST'])
def actualizar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula = Pelicula.obtener_por_id(id)
    if not pelicula or pelicula.usuario_id != session['usuario_id']:
        return redirect('/cine')

    # Almacena los campos ingresados si ocurren errores
    if not Pelicula.validar_pelicula(request.form, pelicula_id=id):
        session['draft_editar'] = request.form
        return redirect(f'/cine/editar/{id}')

    datos = {
        'id': id,
        'titulo': request.form['titulo'].strip(),
        'director': request.form['director'].strip(),
        'fecha_estreno': request.form['fecha_estreno'].strip(),
        'sinopsis': request.form['sinopsis'].strip()
    }
    Pelicula.actualizar(datos)
    return redirect('/cine')

@app.route('/cine/borrar/<int:id>')
def borrar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula = Pelicula.obtener_por_id(id)
    # Solamente borra si el usuario es el creador
    if pelicula and pelicula.usuario_id == session['usuario_id']:
        Pelicula.eliminar(id)

    return redirect('/cine')