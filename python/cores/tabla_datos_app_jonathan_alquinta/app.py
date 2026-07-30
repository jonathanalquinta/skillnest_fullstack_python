from flask import Flask, render_template, request

app = Flask(__name__)

# Datos de las plataformas
PLATAFORMAS = [
    {"nombre": "Discord", "usuarios_num": 250000000, "usuarios_str": "250M", "anio": 2015, "pais": "EE.UU.", "color": "bg-indigo-600"},
    {"nombre": "Instagram", "usuarios_num": 2350000000, "usuarios_str": "2.35B", "anio": 2010, "pais": "EE.UU.", "color": "bg-pink-600"},
    {"nombre": "Netflix", "usuarios_num": 247000000, "usuarios_str": "247M", "anio": 1997, "pais": "EE.UU.", "color": "bg-red-600"},
    {"nombre": "Spotify", "usuarios_num": 515000000, "usuarios_str": "515M", "anio": 2006, "pais": "Suecia", "color": "bg-emerald-500"},
    {"nombre": "TikTok", "usuarios_num": 1700000000, "usuarios_str": "1.7B", "anio": 2016, "pais": "China", "color": "bg-black"},
    {"nombre": "Twitch", "usuarios_num": 140000000, "usuarios_str": "140M", "anio": 2011, "pais": "EE.UU.", "color": "bg-purple-600"},
    {"nombre": "YouTube", "usuarios_num": 2500000000, "usuarios_str": "2.5B", "anio": 2005, "pais": "EE.UU.", "color": "bg-red-500"},
]

@app.route('/')
def index():
    # Obtener parámetros GET del formulario
    pais_filtro = request.args.get('pais', 'Todos los países')
    ordenar_por = request.args.get('ordenar', 'Nombre')
    direccion = request.args.get('direccion', 'Ascendente')

    # Lista única de países para el selector
    paises = ["Todos los países"] + sorted(list(set(p["pais"] for p in PLATAFORMAS)))

    # Filtrar por país
    datos = PLATAFORMAS
    if pais_filtro != 'Todos los países':
        datos = [p for p in datos if p["pais"] == pais_filtro]

    # Mapeo de columna a clave del diccionario
    mapa_orden = {
        'Nombre': 'nombre',
        'Usuarios': 'usuarios_num',
        'Año Fundación': 'anio',
        'País': 'pais'
    }

    campo_clave = mapa_orden.get(ordenar_por, 'nombre')
    es_descendente = (direccion == 'Descendente')

    # Ordenar los datos
    datos_ordenados = sorted(datos, key=lambda x: x[campo_clave], reverse=es_descendente)

    return render_template(
        'index.html',
        plataformas=datos_ordenados,
        paises=paises,
        pais_actual=pais_filtro,
        orden_actual=ordenar_por,
        direccion_actual=direccion
    )

if __name__ == '__main__':
    app.run(debug=True)