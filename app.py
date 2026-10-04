from flask import Flask, request, render_template_string, redirect, url_for
from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)

# Conexión con Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://bkxniuudzmxcpouzgqxm.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_WUzLfoiBMtr7zZknBUo-_w_8W4MwY8S")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    supabase = None

# Plantilla base
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tienda de Ropa - Administración</title>
    <style>
        * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; }
        body { display: flex; min-height: 100vh; background-color: #f7f3f9; }
        
        .sidebar { width: 240px; background-color: #5c08a1; padding: 20px 10px; color: white; display: flex; flex-direction: column; gap: 8px; }
        .sidebar h2 { font-size: 1.2rem; display: flex; align-items: center; gap: 8px; margin-bottom: 2px; }
        .sidebar .subtext { font-size: 0.75rem; color: #d0b0f0; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; }
        .nav-btn { display: flex; align-items: center; gap: 10px; padding: 12px 16px; border-radius: 8px; color: white; text-decoration: none; font-weight: 600; font-size: 0.95rem; border: none; cursor: pointer; transition: opacity 0.2s; }
        .nav-btn:hover { opacity: 0.9; }
        
        .btn-inicio { background-color: #0080ff; }
        .btn-ver { background-color: #28a745; }
        .btn-agregar { background-color: #ffc107; color: #212529; }
        .btn-editar { background-color: #dc3545; }
        .btn-eliminar { background-color: #6f42c1; }
        .btn-buscar { background-color: #17a2b8; }
        .btn-cat { background-color: #fd7e14; }

        .main-content { flex: 1; padding: 40px; }
        .main-content h1 { color: #3a0066; font-size: 2rem; margin-bottom: 8px; }
        .main-content p.desc { color: #666; margin-bottom: 30px; }

        .cards-container { display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap; }
        .card-link { flex: 1; min-width: 200px; text-decoration: none; }
        .card { padding: 25px; border-radius: 12px; color: white; text-align: center; transition: transform 0.2s; }
        .card:hover { transform: translateY(-3px); }
        .card-productos { background: linear-gradient(135deg, #ff8da1, #ff6584); }
        .card-categorias { background: linear-gradient(135deg, #4facfe, #00f2fe); }
        .card-seguridad { background: linear-gradient(135deg, #c792ea, #a17fe0); }
        .card h3 { font-size: 1.3rem; margin: 10px 0 5px; }
        .card p { font-size: 0.85rem; opacity: 0.9; }

        .banner-box { background-color: #ffe5d9; border-radius: 12px; padding: 25px; text-align: center; color: #4a2c2a; }
        .banner-box h3 { font-size: 1.2rem; margin-bottom: 5px; }
        
        .form-box, .table-box { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        input, select { width: 100%; padding: 10px; margin: 8px 0 16px; border: 1px solid #ccc; border-radius: 6px; }
        button.action-btn, a.action-btn { padding: 10px 20px; background-color: #5c08a1; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; text-decoration: none; display: inline-block; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
        th { background-color: #f8f9fa; }
        
        .alert-error { background-color: #f8d7da; color: #721c24; padding: 12px; border-radius: 6px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>👕 Tienda de Ropa</h2>
        <div class="subtext">Administración</div>
        <a href="/" class="nav-btn btn-inicio">🏠 Inicio</a>
        <a href="/productos" class="nav-btn btn-ver">👀 Ver productos</a>
        <a href="/agregar" class="nav-btn btn-agregar">➕ Agregar producto</a>
        <a href="/productos" class="nav-btn btn-editar">✏ Editar producto</a>
        <a href="/productos" class="nav-btn btn-eliminar">🗑️ Eliminar producto</a>
        <a href="/buscar" class="nav-btn btn-buscar">🔍 Buscar producto</a>
        <a href="/categorias" class="nav-btn btn-cat">📁 Ver categorías</a>
    </div>

    <div class="main-content">
        {% if error %}
            <div class="alert-error">
                <strong>Error de conexión / Supabase:</strong> {{ error }}
            </div>
        {% endif %}
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

# ==============================
# PÁGINA PRINCIPAL
# ==============================
@app.route("/")
def index():
    content = """
        <h1>Panel de Administración</h1>
        <p class="desc">Bienvenido al sistema de administración de la tienda.</p>
        
        <div class="cards-container">
            <a href="/productos" class="card-link">
                <div class="card card-productos">
                    <div style="font-size: 2rem;">📦</div>
                    <h3>Productos</h3>
                    <p>Administrar productos</p>
                </div>
            </a>
            <a href="/categorias" class="card-link">
                <div class="card card-categorias">
                    <div style="font-size: 2rem;">📁</div>
                    <h3>Categorías</h3>
                    <p>Consultar categorías</p>
                </div>
            </a>
            <a href="/seguridad" class="card-link">
                <div class="card card-seguridad">
                    <div style="font-size: 2rem;">🛡️</div>
                    <h3>Seguridad</h3>
                    <p>Gestionar Clientes</p>
                </div>
            </a>
        </div>

        <div class="banner-box">
            <h3>👕 Sistema de Tienda de Ropa</h3>
            <p>Desde este panel puedes administrar los productos y categorías de la tienda.</p>
        </div>
    """
    return render_template_string(BASE_TEMPLATE.replace("{% block content %}{% endblock %}", content))

# ==============================
# VER PRODUCTOS
# ==============================
@app.route("/productos")
def ver_productos():
    productos = []
    error_msg = None
    try:
        res = supabase.table("productos").select("*").execute()
        productos = res.data if res.data else []
    except Exception as e:
        error_msg = f"Error al consultar la tabla 'productos': {e}"

    rows = ""
    for p in productos:
        rows += f"""
        <tr>
            <td>#{p.get('id')}</td>
            <td>{p.get('nombre')}</td>
            <td>${p.get('precio')}</td>
            <td>
                <a href="/editar/{p.get('id')}" style="color: #dc3545; text-decoration: none; font-weight: bold; margin-right: 10px;">Editar</a>
                <form method="POST" action="/eliminar/{p.get('id')}" style="display:inline;">
                    <button type="submit" style="background:none; border:none; color:#6f42c1; cursor:pointer; font-weight:bold;" onclick="return confirm('¿Eliminar producto?');">Eliminar</button>
                </form>
            </td>
        </tr>
        """

    content = f"""
        <h1>Lista de Productos</h1>
        <p class="desc">Consulta y gestiona el inventario de la tienda.</p>
        <div class="table-box">
            <table>
                <thead>
                    <tr><th>ID</th><th>Nombre</th><th>Precio</th><th>Acciones</th></tr>
                </thead>
                <tbody>
                    {rows if rows else '<tr><td colspan="4">No hay productos registrados.</td></tr>'}
                </tbody>
            </table>
        </div>
    """
    return render_template_string(BASE_TEMPLATE.replace("{% block content %}{% endblock %}", content), error=error_msg)

# ==============================
# SEGURIDAD (TABLA CLIENTES)
# ==============================
@app.route("/seguridad")
def seguridad():
    clientes = []
    error_msg = None
    try:
        res = supabase.table("clientes").select("*").execute()
        clientes = res.data if res.data else []
    except Exception as e:
        error_msg = f"Error al consultar la tabla 'clientes': {e}"

    rows = ""
    for c in clientes:
        # Muestra dinámicamente los campos según lo que tenga tu tabla clientes
        nombre = c.get('nombre') or c.get('nombre_cliente') or c.get('email') or 'Sin Nombre'
        correo = c.get('email') or c.get('correo') or 'N/A'
        
        rows += f"""
        <tr>
            <td>#{c.get('id')}</td>
            <td>{nombre}</td>
            <td>{correo}</td>
        </tr>
        """

    content = f"""
        <h1>Panel de Seguridad</h1>
        <p class="desc">Gestión de acceso y clientes registrados en el sistema.</p>

        <div class="table-box">
            <h3>Clientes Registrados</h3>
            <table>
                <thead>
                    <tr><th>ID</th><th>Cliente</th><th>Correo</th></tr>
                </thead>
                <tbody>
                    {rows if rows else '<tr><td colspan="3">No hay clientes registrados en la tabla.</td></tr>'}
                </tbody>
            </table>
        </div>
        <br>
        <a href="/" class="action-btn">Volver al Inicio</a>
    """
    return render_template_string(BASE_TEMPLATE.replace("{% block content %}{% endblock %}", content), error=error_msg)

# ==============================
# CATEGORÍAS (TABLA CATEGORIAS)
# ==============================
@app.route("/categorias")
def categorias():
    cats = []
    error_msg = None
    try:
        res = supabase.table("categorias").select("*").execute()
        cats = res.data if res.data else []
    except Exception as e:
        error_msg = f"Error al consultar la tabla 'categorias': {e}"

    rows = ""
    for cat in cats:
        rows += f"""
        <tr>
            <td>#{cat.get('id')}</td>
            <td>{cat.get('nombre') or cat.get('nombre_categoria') or 'Sin Nombre'}</td>
        </tr>
        """

    content = f"""
        <h1>Categorías de Productos</h1>
        <p class="desc">Consulta las categorías disponibles en la tienda.</p>

        <div class="table-box">
            <table>
                <thead>
                    <tr><th>ID</th><th>Categoría</th></tr>
                </thead>
                <tbody>
                    {rows if rows else '<tr><td colspan="2">No hay categorías registradas.</td></tr>'}
                </tbody>
            </table>
        </div>
        <br>
        <a href="/" class="action-btn">Volver al Inicio</a>
    """
    return render_template_string(BASE_TEMPLATE.replace("{% block content %}{% endblock %}", content), error=error_msg)

# ==============================
# AGREGAR PRODUCTO
# ==============================
@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    error_msg = None
    if request.method == "POST":
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        try:
            supabase.table("productos").insert({"nombre": nombre, "precio": float(precio)}).execute()
            return redirect(url_for("ver_productos"))
        except Exception as e:
            error_msg = f"Error al guardar producto: {e}"

    content = f"""
        <h1>Agregar Producto</h1>
        <p class="desc">Ingresa los datos para registrar una nueva prenda.</p>
        <div class="form-box">
            <form method="POST">
                <label>Nombre del producto:</label>
                <input type="text" name="nombre" placeholder="Ej. Camiseta Algodón" required>
                <label>Precio ($):</label>
                <input type="number" step="0.01" name="precio" placeholder="Ej. 199.99" required>
                <button type="submit" class="action-btn">Guardar Producto</button>
            </form>
        </div>
    """
    return render_template_string(BASE_TEMPLATE.replace("{% block content %}{% endblock %}", content), error=error_msg)

# ==============================
# EDITAR PRODUCTO
# ==============================
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    error_msg = None
    if request.method == "POST":
        nuevo_nombre = request.form.get("nombre")
        nuevo_precio = request.form.get("precio")
        try:
            supabase.table("productos").update({"nombre": nuevo_nombre, "precio": float(nuevo_precio)}).eq("id", id).execute()
            return redirect(url_for("ver_productos"))
        except Exception as e:
            error_msg = f"Error al actualizar: {e}"

    producto = {}
    try:
        res = supabase.table("productos").select("*").eq("id", id).execute()
        if res.data:
            producto = res.data[0]
    except Exception as e:
        error_msg = f"Error al obtener producto: {e}"

    content = f"""
        <h1>Editar Producto</h1>
        <p class="desc">Modifica los detalles del producto #{id}.</p>
        <div class="form-box">
            <form method="POST">
                <label>Nombre del producto:</label>
                <input type="text" name="nombre" value="{producto.get('nombre', '')}" required>
                <label>Precio ($):</label>
                <input type="number" step="0.01" name="precio" value="{producto.get('precio', '')}" required>
                <button type="submit" class="action-btn">Actualizar Producto</button>
            </form>
        </div>
    """
    return render_template_string(BASE_TEMPLATE.replace("{% block content %}{% endblock %}", content), error=error_msg)

# ==============================
# ELIMINAR PRODUCTO
# ==============================
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    try:
        supabase.table("productos").delete().eq("id", id).execute()
    except Exception as e:
        pass
    return redirect(url_for("ver_productos"))

# ==============================
# BUSCAR PRODUCTO
# ==============================
@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    resultados = []
    busqueda = ""
    error_msg = None
    if request.method == "POST":
        busqueda = request.form.get("busqueda", "")
        try:
            res = supabase.table("productos").select("*").ilike("nombre", f"%{busqueda}%").execute()
            resultados = res.data if res.data else []
        except Exception as e:
            error_msg = f"Error al realizar la búsqueda: {e}"

    rows = ""
    for p in resultados:
        rows += f"<tr><td>#{p.get('id')}</td><td>{p.get('nombre')}</td><td>${p.get('precio')}</td></tr>"

    content = f"""
        <h1>Buscar Producto</h1>
        <p class="desc">Encuentra productos por su nombre.</p>
        <div class="form-box" style="margin-bottom: 20px;">
            <form method="POST">
                <input type="text" name="busqueda" value="{busqueda}" placeholder="Escribe el nombre del producto..." required>
                <button type="submit" class="action-btn">Buscar</button>
            </form>
        </div>
        
        {f'''
        <div class="table-box">
            <table>
                <thead><tr><th>ID</th><th>Nombre</th><th>Precio</th></tr></thead>
                <tbody>{rows if rows else '<tr><td colspan="3">No se encontraron coincidencias.</td></tr>'}</tbody>
            </table>
        </div>
        ''' if request.method == "POST" else ''}
    """
    return render_template_string(BASE_TEMPLATE.replace("{% block content %}{% endblock %}", content), error=error_msg)

if __name__ == "__main__":
    app.run(debug=True)
