from flask import redirect, request, session, flash
from flask_app import app
from flask_app.models.comentario import Comentario
from flask_app.models.pelicula import Pelicula

@app.route('/comentarios/crear', methods=['POST'])
def crear_comentario():
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula_id = request.form.get('pelicula_id')
    pelicula = Pelicula.obtener_por_id(pelicula_id)

    # Un usuario no puede comentar su propia película
    if pelicula and pelicula.usuario_id == session['usuario_id']:
        flash("Un usuario no puede comentar su propia película.", "error_comentario")
        return redirect(f'/cine/{pelicula_id}')

    contenido = request.form.get('contenido', '').strip()
    if not contenido:
        return redirect(f'/cine/{pelicula_id}')

    datos = {
        'contenido': contenido,
        'usuario_id': session['usuario_id'],
        'pelicula_id': pelicula_id
    }
    Comentario.guardar(datos)
    return redirect(f'/cine/{pelicula_id}')

@app.route('/comentarios/borrar/<int:id>')
def borrar_comentario(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pelicula_id = request.args.get('pelicula_id')
    comentario = Comentario.obtener_por_id(id)

    # El botón y acción de borrar le pertenece solo al dueño del comentario
    if comentario and comentario.usuario_id == session['usuario_id']:
        Comentario.eliminar(id)

    return redirect(f'/cine/{pelicula_id}' if pelicula_id else '/cine')