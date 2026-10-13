from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.pelicula import Pelicula

@app.route('/cine')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    # Lógica para obtener películas...
    return render_template('dashboard.html')