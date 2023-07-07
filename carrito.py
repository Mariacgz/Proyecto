import pymysql
from flask import Flask, jsonify, request, render_templates

from flask_cors import CORS

# Función para obtener la conexión a la base de datos
def get_db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="mibasededatos",
        port=3307
    )



# Crear la base de datos si no existe
def crear_basededatos():
    try:
        cursor = conexion.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS mibasededatos")
        cursor.close()
        print("La base de datos 'mibasededatos' ha sido creada, o ya existía.")
    except pymysql.Error as e:
        print(f"Error al crear la base de datos: {e}")

# Crear la tabla 'productos' si no existe
def crear_tabla_productos():
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                codigo INT PRIMARY KEY AUTO_INCREMENT,
                descripcion VARCHAR(255),
                stock INT,
                precio FLOAT
            )
        """)
        cursor.close()
        print("La tabla 'productos' ha sido creada, o ya existía.")
    except pymysql.Error as e:
        print(f"Error al crear la tabla 'productos': {e}")
        

# -------------------------------------------------------------------
# Definimos la clase "Producto"
# -------------------------------------------------------------------
class Producto:
    def __init__(self, codigo, descripcion, cantidad, precio):
        self.codigo = codigo
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio = precio

    def modificar(self, nueva_descripcion, nueva_cantidad, nuevo_precio):
        self.descripcion = nueva_descripcion
        self.cantidad = nueva_cantidad
        self.precio = nuevo_precio


# -------------------------------------------------------------------
# Definimos la clase "Inventario"
# -------------------------------------------------------------------
class Inventario:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    def agregar_producto(self, codigo, descripcion, cantidad, precio):
        producto_existente = self.consultar_producto(codigo)
        if producto_existente:
            return jsonify({'message': 'Ya existe un producto con ese código.'}), 400

        nuevo_producto = Producto(codigo, descripcion, cantidad, precio)
        self.cursor.execute("INSERT INTO productos VALUES (?, ?, ?, ?)", (codigo, descripcion, cantidad, precio))
        self.conexion.commit()
        return jsonify({'message': 'Producto agregado correctamente.'}), 200

    def consultar_producto(self, codigo):
        self.cursor.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
        row = self.cursor.fetchone()
        if row:
            codigo, descripcion, cantidad, precio = row
            return Producto(codigo, descripcion, cantidad, precio)
        return None

    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio):
        producto = self.consultar_producto(codigo)
        if producto:
            producto.modificar(nueva_descripcion, nueva_cantidad, nuevo_precio)
            self.cursor.execute("UPDATE productos SET descripcion = ?, cantidad = ?, precio = ? WHERE codigo = ?",
                                (nueva_descripcion, nueva_cantidad, nuevo_precio, codigo))
            self.conexion.commit()
            return jsonify({'message': 'Producto modificado correctamente.'}), 200
        return jsonify({'message': 'Producto no encontrado.'}), 404

    def listar_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        rows = self.cursor.fetchall()
        productos = []
        for row in rows:
            codigo, descripcion, cantidad, precio = row
            producto = {'codigo': codigo, 'descripcion': descripcion, 'cantidad': cantidad, 'precio': precio}
            productos.append(producto)
        return jsonify(productos), 200

    def eliminar_producto(self, codigo):
        self.cursor.execute("DELETE FROM productos WHERE codigo = ?", (codigo,))
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Producto eliminado correctamente.'}), 200
        return jsonify({'message': 'Producto no encontrado.'}), 404


# -------------------------------------------------------------------
# Definimos la clase "Carrito"
# -------------------------------------------------------------------
class Carrito:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()
        self.items = []

    def agregar(self, codigo, cantidad, inventario):
        producto = inventario.consultar_producto(codigo)
        if producto is None:
            return jsonify({'message': 'El producto no existe.'}), 404
        if producto.cantidad < cantidad:
            return jsonify({'message': 'Cantidad en stock insuficiente.'}), 400

        for item in self.items:
            if item.codigo == codigo:
                item.cantidad += cantidad
                self.cursor.execute("UPDATE productos SET cantidad = cantidad - ? WHERE codigo = ?",
                                    (cantidad, codigo))
                self.conexion.commit()
                return jsonify({'message': 'Producto agregado al carrito correctamente.'}), 200

        nuevo_item = Producto(codigo, producto.descripcion, cantidad, producto.precio)
        self.items.append(nuevo_item)
        self.cursor.execute("UPDATE productos SET cantidad = cantidad - ? WHERE codigo = ?",
                            (cantidad, codigo))
        self.conexion.commit()
        return jsonify({'message': 'Producto agregado al carrito correctamente.'}), 200

    def quitar(self, codigo, cantidad, inventario):
        for item in self.items:
            if item.codigo == codigo:
                if cantidad > item.cantidad:
                    return jsonify({'message': 'Cantidad a quitar mayor a la cantidad en el carrito.'}), 400
                item.cantidad -= cantidad
                if item.cantidad == 0:
                    self.items.remove(item)
                self.cursor.execute("UPDATE productos SET cantidad = cantidad + ? WHERE codigo = ?",
                                    (cantidad, codigo))
                self.conexion.commit()
                return jsonify({'message': 'Producto quitado del carrito correctamente.'}), 200

        return jsonify({'message': 'El producto no se encuentra en el carrito.'}), 404

    def mostrar(self):
        productos_carrito = []
        for item in self.items:
            producto = {'codigo': item.codigo, 'descripcion': item.descripcion, 'cantidad': item.cantidad,
                        'precio': item.precio}
            productos_carrito.append(producto)
        return jsonify(productos_carrito), 200


# -------------------------------------------------------------------
# Configuración y rutas de la API Flask
# -------------------------------------------------------------------

app = Flask(__name__)
CORS(app)

# ...

# Ruta para obtener los datos de un producto según su código
@app.route('/productos/<int:codigo>', methods=['GET'])
def obtener_producto(codigo):
    producto = inventario.consultar_producto(codigo)
    if producto:
        response = {
            'codigo': producto.codigo,
            'descripcion': producto.descripcion,
            'cantidad': producto.cantidad,
            'precio': producto.precio
        }
        return jsonify(response), 200
    return jsonify({'message': 'Producto no encontrado.'}), 404

# Ruta para obtener la lista de productos del inventario
@app.route('/productos', methods=['GET'])
def obtener_productos():
    response = inventario.listar_productos()
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5501')
    return response

# Ruta para agregar un producto al inventario
@app.route('/productos', methods=['POST'])
def agregar_producto():
    codigo = request.json.get('codigo')
    descripcion = request.json.get('descripcion')
    cantidad = request.json.get('cantidad')
    precio = request.json.get('precio')
    response = inventario.agregar_producto(codigo, descripcion, cantidad, precio)
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5501')
    return response

# Ruta para modificar un producto del inventario
@app.route('/productos/<int:codigo>', methods=['PUT'])
def modificar_producto(codigo):
    nueva_descripcion = request.json.get('descripcion')
    nueva_cantidad = request.json.get('cantidad')
    nuevo_precio = request.json.get('precio')
    response = inventario.modificar_producto(codigo, nueva_descripcion, nueva_cantidad, nuevo_precio)
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5501')
    return response

# Ruta para eliminar un producto del inventario
@app.route('/productos/<int:codigo>', methods=['DELETE'])
def eliminar_producto(codigo):
    response = inventario.eliminar_producto(codigo)
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5501')
    return response

# Ruta para agregar un producto al carrito
@app.route('/carrito', methods=['POST'])
def agregar_carrito():
    codigo = request.json.get('codigo')
    cantidad = request.json.get('cantidad')
    inventario = Inventario()
    response = carrito.agregar(codigo, cantidad, inventario)
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5501')
    return response

# Ruta para quitar un producto del carrito
@app.route('/carrito', methods=['DELETE'])
def quitar_carrito():
    codigo = request.json.get('codigo')
    cantidad = request.json.get('cantidad')
    inventario = Inventario()
    response = carrito.quitar(codigo, cantidad, inventario)
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5501')
    return response

# Ruta para obtener el contenido del carrito
@app.route('/carrito', methods=['GET'])
def obtener_carrito():
    response = carrito.mostrar()
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5501')
    return response

# Ruta para obtener la lista de productos del inventario
@app.route('/')
def index():
    return render_templates("index.html")

# ...

# Finalmente, si estamos ejecutando este archivo, lanzamos app.
if __name__ == '__main__':
    app.run()