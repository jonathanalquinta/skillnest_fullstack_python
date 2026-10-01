from app import app
from app.controllers import controlador_usuarios, controlador_libros

if __name__ == "__main__":
    app.run(debug=True)