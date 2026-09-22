from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/productos")
def productos():
    return "<h1>Lista de productos</h1><a href='/'>Regresar</a>"


@app.route("/agregar")
def agregar():
    return "<h1>Agregar producto</h1><a href='/'>Regresar</a>"


@app.route("/editar")
def editar():
    return "<h1>Editar producto</h1><a href='/'>Regresar</a>"


@app.route("/eliminar")
def eliminar():
    return "<h1>Eliminar producto</h1><a href='/'>Regresar</a>"


@app.route("/buscar")
def buscar():
    return "<h1>Buscar producto</h1><a href='/'>Regresar</a>"


@app.route("/categorias")
def categorias():
    return "<h1>Categorías</h1><a href='/'>Regresar</a>"


if __name__ == "__main__":
    app.run(debug=True)
