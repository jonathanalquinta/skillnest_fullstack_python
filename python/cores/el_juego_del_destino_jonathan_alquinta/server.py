import random
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "clave_secreta"

PREDICCIONES = [
    "Encontrarás el verdadero amor en los próximos meses. Tu corazón se llenará de alegría.",
    "Un giro inesperado en tus decisiones te traerá una gran racha de buena suerte.",
    "Ten cuidado con las decisiones apresuradas esta semana; tómate un tiempo para reflexionar.",
    "Una gran oportunidad profesional tocará a tu puerta cuando menos lo esperes.",
    "Un pequeño obstáculo pondrá a prueba tu paciencia, pero saldrás más fuerte."
]

SIGNIFICADOS_COLOR = {
    "rojo": "fuerza y pasión indomable",
    "azul": "serenidad y claridad mental",
    "verde": "misterio y descubrimiento",
    "morado": "intuición y creatividad",
    "amarillo": "energía y brillantez"
}

SIGNIFICADOS_ANIMAL = {
    "perro": "lealtad e intuición protectora",
    "gato": "independencia y misterio",
    "águila": "visión elevada y libertad",
    "león": "valentía y liderazgo natural",
    "delfín": "armonía y gran empatía"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/enviar", methods=["POST"])
def enviar():
    session["nombre"] = request.form.get("nombre", "").strip()
    session["edad"] = request.form.get("edad", "").strip()
    session["color"] = request.form.get("color", "").strip().lower()
    session["animal"] = request.form.get("animal", "").strip().lower()
    
    session["numero_suerte"] = random.randint(1, 99)
    session["prediccion"] = random.choice(PREDICCIONES)
    
    return redirect(url_for("futuro"))

@app.route("/futuro")
def futuro():
    if "nombre" not in session:
        return redirect(url_for("index"))

    color_usuario = session.get("color", "verde")
    animal_usuario = session.get("animal", "gato")

    sig_color = SIGNIFICADOS_COLOR.get(color_usuario, "misterio y transformación")
    sig_animal = SIGNIFICADOS_ANIMAL.get(animal_usuario, "independencia y destreza")

    return render_template(
        "futuro.html",
        nombre=session.get("nombre"),
        edad=session.get("edad"),
        color=color_usuario,
        animal=animal_usuario,
        numero_suerte=session.get("numero_suerte"),
        prediccion=session.get("prediccion"),
        sig_color=sig_color,
        sig_animal=sig_animal
    )

if __name__ == "__main__":
    app.run(debug=True)