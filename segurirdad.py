import psycopg2
from psycopg2 import Error
from decimal import Decimal
# CONFIGURACIÓN
DATABASE_URL = "postgresql://neondb_owner:npg_ogsaYUyHuP53@ep-young-feather-ayvl8tvh-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
# CONEXIÓN A NEON
def conectar():
    try:
        conexion = psycopg2.connect(DATABASE_URL)
        return conexion
    except Error as e:
        print("❌ Error al conectar con Neon:")
        print(e)
        return None
# MOSTRAR PRODUCTOS
def mostrar_productos():
    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                p.id,
                p.nombre,
                p.descripcion,
                p.precio,
                p.stock,
                p.talla,
                p.color,
                c.nombre AS categoria
            FROM productos p
            LEFT JOIN categorias c
                ON p.categoria_id = c.id
            ORDER BY p.id;
        """)
        productos = cursor.fetchall()
        print("\n" + "=" * 100)
        print("LISTA DE PRODUCTOS")
        print("=" * 100)
        if not productos:
            print("No hay productos registrados.")
            return
        for producto in productos:
            id_producto = producto[0]
            nombre = producto[1]
            descripcion = producto[2]
            precio = producto[3]
            stock = producto[4]
            talla = producto[5]
            color = producto[6]
            categoria = producto[7]
            print(f"""
ID:          {id_producto}
Nombre:      {nombre}
Descripción: {descripcion}
Precio:      ${precio}
Stock:       {stock}
Talla:       {talla}
Color:       {color}
Categoría:   {categoria}
{"-" * 60}
""")
    except Error as e:
        print("❌ Error:", e)
    finally:
        cursor.close()
        conexion.close()
# MOSTRAR CATEGORÍAS
def mostrar_categorias():
    conexion = conectar()
    if conexion is None:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, nombre
            FROM categorias
            ORDER BY id;
        """)
        categorias = cursor.fetchall()
        print("\n" + "=" * 50)
        print("CATEGORÍAS")
        print("=" * 50)
        for categoria in categorias:
            print(f"{categoria[0]} → {categoria[1]}")
        return categorias
    except Error as e:
        print("❌ Error:", e)
        return []
    finally:
        cursor.close()
        conexion.close()
# AGREGAR PRODUCTO
def agregar_producto():
    print("\n")
    print("=" * 50)
    print("AGREGAR PRODUCTO")
    print("=" * 50)
    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción: ")
    while True:
        try:
            precio = float(input("Precio: "))
            if precio < 0:
                print("❌ El precio no puede ser negativo.")
                continue
            break
        except ValueError:
            print("❌ Introduce un número válido.")
    while True:
        try:
            stock = int(input("Stock: "))
            if stock < 0:
                print("❌ El stock no puede ser negativo.")
                continue
            break
        except ValueError:
            print("❌ Introduce un número entero.")
    talla = input("Talla: ")
    color = input("Color: ")
    mostrar_categorias()
    while True:
        try:
            categoria_id = int(input("ID de la categoría: "))
            break
        except ValueError:
            print("❌ Introduce un número válido.")
    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO productos
            (
                nombre,
                descripcion,
                precio,
                stock,
                talla,
                color,
                categoria_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            nombre,
            descripcion,
            precio,
            stock,
            talla,
            color,
            categoria_id
        ))

        nuevo_id = cursor.fetchone()[0]
        conexion.commit()
        print(f"\n✅ Producto agregado correctamente.")
        print(f"ID del producto: {nuevo_id}")
    except Error as e:
        conexion.rollback()
        print("❌ Error al agregar producto:")
        print(e)
    finally:
        cursor.close()
        conexion.close()
# EDITAR PRODUCTO
def editar_producto():
    print("\n")
    print("=" * 50)
    print("EDITAR PRODUCTO")
    print("=" * 50)
    mostrar_productos()
    try:
        producto_id = int(input("Introduce el ID del producto que quieres editar: "))
    except ValueError:
        print("❌ ID inválido.")
        return
    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                nombre,
                descripcion,
                precio,
                stock,
                talla,
                color,
                categoria_id
            FROM productos
            WHERE id = %s;
        """, (producto_id,))
        producto = cursor.fetchone()
        if producto is None:
            print("❌ No existe un producto con ese ID.")
            return
        print("\nDeja vacío un campo si quieres conservar su valor actual.")
        nombre = input(f"Nombre [{producto[0]}]: ")
        descripcion = input(f"Descripción [{producto[1]}]: ")
        precio = input(f"Precio [{producto[2]}]: ")
        stock = input(f"Stock [{producto[3]}]: ")
        talla = input(f"Talla [{producto[4]}]: ")
        color = input(f"Color [{producto[5]}]: ")
        categoria = input(f"ID categoría [{producto[6]}]: ")
        if nombre == "":
            nombre = producto[0]
        if descripcion == "":
            descripcion = producto[1]
        if precio == "":
            precio = producto[2]
        else:
            precio = float(precio)
        if stock == "":
            stock = producto[3]
        else:
            stock = int(stock)
        if talla == "":
            talla = producto[4]
        if color == "":
            color = producto[5]
        if categoria == "":
            categoria = producto[6]
        else:
            categoria = int(categoria)
        cursor.execute("""
            UPDATE productos
            SET
                nombre = %s,
                descripcion = %s,
                precio = %s,
                stock = %s,
                talla = %s,
                color = %s,
                categoria_id = %s
            WHERE id = %s;
        """, (
            nombre,
            descripcion,
            precio,
            stock,
            talla,
            color,
            categoria,
            producto_id
        ))

        conexion.commit()

        print("\n✅ Producto actualizado correctamente.")

    except ValueError:

        conexion.rollback()
        print("❌ Introdujiste un valor incorrecto.")
    except Error as e:
        conexion.rollback()
        print("❌ Error al actualizar:")
        print(e)
    finally:
        cursor.close()
        conexion.close()
# ELIMINAR PRODUCTO
def eliminar_producto():
    print("\n")
    print("=" * 50)
    print("ELIMINAR PRODUCTO")
    print("=" * 50)
    mostrar_productos()
    try:
        producto_id = int(
            input("Introduce el ID del producto que quieres eliminar: ")
        )
    except ValueError:
        print("❌ ID inválido.")
        return
    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT nombre
            FROM productos
            WHERE id = %s;
        """, (producto_id,))
        producto = cursor.fetchone()
        if producto is None:
            print("❌ Ese producto no existe.")
            return
        print(f"\nProducto seleccionado: {producto[0]}")
        confirmar = input(
            "¿Seguro que quieres eliminarlo? (s/n): "
        ).lower()
        if confirmar != "s":
            print("❌ Operación cancelada.")
            return
        cursor.execute("""
            DELETE FROM productos
            WHERE id = %s;
        """, (producto_id,))
        conexion.commit()
        print("\n✅ Producto eliminado correctamente.")
    except Error as e:
        conexion.rollback()
        print("❌ Error al eliminar:")
        print(e)
    finally:
        cursor.close()
        conexion.close()
# BUSCAR PRODUCTO
def buscar_producto():
    print("\n")
    print("=" * 50)
    print("BUSCAR PRODUCTO")
    print("=" * 50)
    texto = input("Escribe el nombre del producto: ")
    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                p.id,
                p.nombre,
                p.precio,
                p.stock,
                p.talla,
                p.color,
                c.nombre
            FROM productos p
            LEFT JOIN categorias c
                ON p.categoria_id = c.id
            WHERE p.nombre ILIKE %s
            ORDER BY p.id;
        """, (f"%{texto}%",))

        productos = cursor.fetchall()

        if not productos:

            print("\n❌ No encontramos productos.")

        else:

            print("\nProductos encontrados:\n")

            for producto in productos:

                print(
                    f"ID: {producto[0]} | "
                    f"{producto[1]} | "
                    f"${producto[2]} | "
                    f"Stock: {producto[3]} | "
                    f"Talla: {producto[4]} | "
                    f"Color: {producto[5]} | "
                    f"Categoría: {producto[6]}"
                )
    except Error as e:
        print("❌ Error:", e)
    finally:
        cursor.close()
        conexion.close()
# MENÚ PRINCIPAL
def menu():
    while True:
        print("\n")
        print("=" * 60)
        print("       👕 TIENDA DE ROPA - ADMINISTRACIÓN")
        print("=" * 60)
        print("1. 👀 Ver productos")
        print("2. ➕ Agregar producto")
        print("3. ✏️ Editar producto")
        print("4. 🗑️ Eliminar producto")
        print("5. 🔎 Buscar producto")
        print("6. 📂 Ver categorías")
        print("7. 🚪 Salir")
        print("=" * 60)
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            mostrar_productos()
        elif opcion == "2":
            agregar_producto()
        elif opcion == "3":
            editar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            buscar_producto()
        elif opcion == "6":
            mostrar_categorias()
        elif opcion == "7":
            print("\n👋 Programa terminado.")
            break
        else:
            print("\n❌ Opción no válida.")
# INICIAR PROGRAMA
print("Conectando con Neon...")
conexion_prueba = conectar()
if conexion_prueba:
    print("✅ Conexión exitosa con Neon.")
    conexion_prueba.close()
    menu()
else:
    print("❌ No se pudo conectar a Neon.")
    print("Revisa tu DATABASE_URL.")
