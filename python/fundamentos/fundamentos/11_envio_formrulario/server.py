"""
===========================================
Formulario de Prueba
===========================================
"""

from flask import (
    Flask,
    render_template,
    request,
    redirect
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():
    print("========== NUEVO USUARIO ==========")
    print(request.form)
    print("-----------------------------------")
    print("Nombre:", request.form["nombre"])
    print("Correo:", request.form["email"])
    print("===================================")

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)