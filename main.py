from flask import Flask, request, jsonify
import pymysql
import logging

app = Flask(__name__)


logging.basicConfig(level=logging.INFO)  # Configura el nivel de log
logger = logging.getLogger(__name__)

# Configuración de la base de datos
try:
    db = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="6991",
    database="parcial_python"
    )
    logger.info('Conexión a la base de datos exitosa.')
except Exception as e:
    logger.error(f'Error al conectar a la base de datos: {e}')

# Crear la tabla 'items' en la base de datos
with db.cursor() as cursor:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        )
    ''')
    db.commit()

# Ruta para obtener todos los elementos
@app.route('/items', methods=['GET'])
def get_items():
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
    return jsonify({'items': items})

# Ruta para obtener un elemento por su ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM items WHERE id=%s', item_id)
        item = cursor.fetchone()
    return jsonify({'item': item})

# Ruta para agregar un nuevo elemento
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    name = data['name']
    price = data['price']

    with db.cursor() as cursor:
        cursor.execute('INSERT INTO items (name, price) VALUES (%s, %s)', (name, price))
        db.commit()

    return jsonify({'message': 'Item agregado con éxito'})

# Ruta para actualizar un elemento
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    name = data['name']
    price = data['price']

    with db.cursor() as cursor:
        cursor.execute('UPDATE items SET name=%s, price=%s WHERE id=%s', (name, price, item_id))
        db.commit()

    return jsonify({'message': 'Item actualizado con éxito'})

# Ruta para eliminar un elemento
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    with db.cursor() as cursor:
        cursor.execute('DELETE FROM items WHERE id=%s', item_id)
        db.commit()

    return jsonify({'message': 'Item eliminado con éxito'})

if __name__ == '__main__':
    app.run(debug=True)