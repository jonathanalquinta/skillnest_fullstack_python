from flask import render_template, request, redirect, session, flash
from app import app
from app.models.modelo_libro import Libro

@app.route('/libros')
def mis_libros():
    if 'usuario_id' not in session:
        return redirect('/')
    
    mis_libros = Libro.obtener_por_usuario(session['usuario_id'])
    libros_comunidad = Libro.obtener_comunidad(session['usuario_id'])
    
    return render_template('books/mis_libros.html', mis_libros=mis_libros, comunidad=libros_comunidad)

@app.route('/libros/nuevo', methods=['GET', 'POST'])
def nuevo_libro():
    if 'usuario_id' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        if not Libro.validar_libro(request.form):
            return redirect('/libros/nuevo')

        datos = {
            'titulo': request.form['titulo'],
            'autor': request.form['autor'],
            'genero': request.form['genero'],
            'fecha_publicacion': request.form['fecha_publicacion'],
            'descripcion': request.form['descripcion'],
            'usuario_id': session['usuario_id']
        }
        Libro.guardar(datos)
        return redirect('/libros')

    return render_template('books/nuevo_libro.html')

@app.route('/libros/<int:id>')
def detalle_libro(id):
    if 'usuario_id' not in session:
        return redirect('/')

    libro = Libro.obtener_por_id(id)
    if not libro:
        return redirect('/libros')

    es_fav = Libro.es_favorito(session['usuario_id'], id)
    usuarios_fav = Libro.obtener_usuarios_que_agregaron_favorito(id)

    return render_template('books/detalle_libro.html', libro=libro, es_favorito=es_fav, usuarios_fav=usuarios_fav)

@app.route('/libros/editar/<int:id>', methods=['GET', 'POST'])
def editar_libro(id):
    if 'usuario_id' not in session:
        return redirect('/')

    libro = Libro.obtener_por_id(id)
    
    if not libro or libro.usuario_id != session['usuario_id']:
        flash("No tienes permiso para editar este libro.", "error")
        return redirect('/libros')

    if request.method == 'POST':
        if not Libro.validar_libro(request.form):
            return redirect(f'/libros/editar/{id}')

        datos = {
            'id': id,
            'titulo': request.form['titulo'],
            'autor': request.form['autor'],
            'genero': request.form['genero'],
            'fecha_publicacion': request.form['fecha_publicacion'],
            'descripcion': request.form['descripcion'],
            'usuario_id': session['usuario_id']
        }
        Libro.actualizar(datos)
        return redirect('/libros')

    return render_template('books/editar_libro.html', libro=libro)

@app.route('/libros/borrar/<int:id>')
def borrar_libro(id):
    if 'usuario_id' not in session:
        return redirect('/')

    Libro.eliminar(id, session['usuario_id'])
    return redirect('/libros')

@app.route('/favoritos')
def favoritos():
    if 'usuario_id' not in session:
        return redirect('/')

    libros_fav = Libro.obtener_favoritos_usuario(session['usuario_id'])
    return render_template('favoritos.html', libros=libros_fav)

@app.route('/favoritos/agregar/<int:libro_id>', methods=['POST'])
def agregar_favorito(libro_id):
    if 'usuario_id' not in session:
        return redirect('/')

    Libro.agregar_favorito(session['usuario_id'], libro_id)
    return redirect(f'/libros/{libro_id}')