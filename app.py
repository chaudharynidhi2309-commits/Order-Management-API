from flask import Flask, request, jsonify
from flasgger import Swagger
from db_config import get_db_connection, release_db_connection

app = Flask(__name__)

# Swagger Configuration
app.config['SWAGGER'] = {
    'title': 'Complete Order Management API - Nidhi Chaudhary',
    'uiversion': 3
}
swagger = Swagger(app)

@app.route('/orders', methods=['GET'])
def get_orders():
    """
    1. VIEW ALL ORDERS (Read)
    ---
    responses:
      200:
        description: List of all orders
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders ORDER BY id ASC;")
    rows = cur.fetchall()
    cur.close()
    release_db_connection(conn)
    orders = [{"id": r[0], "customer": r[1], "product": r[2], "price": float(r[3]), "qty": r[4], "status": r[5]} for r in rows]
    return jsonify(orders)

@app.route('/orders/search', methods=['GET'])
def search_orders():
    """
    2. SEARCH BY NAME (Extra Read)
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: true
    responses:
      200:
        description: Filtered orders
    """
    name = request.args.get('name')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE customer_name ILIKE %s;", (f"%{name}%",))
    rows = cur.fetchall()
    cur.close()
    release_db_connection(conn)
    orders = [{"id": r[0], "customer": r[1], "product": r[2], "price": float(r[3]), "qty": r[4], "status": r[5]} for r in rows]
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def add_order():
    """
    3. PLACE ORDER (Create)
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            customer_name: {type: string}
            product_name: {type: string}
            price: {type: number}
            quantity: {type: integer}
    responses:
      201:
        description: Order created
    """
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (customer_name, product_name, price, quantity) VALUES (%s, %s, %s, %s) RETURNING id;",
        (data['customer_name'], data['product_name'], data['price'], data['quantity'])
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    release_db_connection(conn)
    return jsonify({"message": "Order created", "id": new_id}), 201

@app.route('/orders/status/<int:order_id>', methods=['PUT'])
def update_status(order_id):
    """
    4. UPDATE STATUS (Update)
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
      - name: body
        in: body
        schema:
          properties:
            status: {type: string, example: "Shipped"}
    responses:
      200:
        description: Status updated
    """
    data = request.get_json()
    new_status = data.get('status')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status = %s WHERE id = %s;", (new_status, order_id))
    conn.commit()
    cur.close()
    release_db_connection(conn)
    return jsonify({"message": "Status updated"})

@app.route('/orders/quantity/<int:order_id>', methods=['PUT'])
def update_quantity(order_id):
    """
    5. UPDATE QUANTITY (Extra Update)
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
      - name: body
        in: body
        schema:
          properties:
            quantity: {type: integer}
    responses:
      200:
        description: Quantity updated
    """
    data = request.get_json()
    new_qty = data.get('quantity')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET quantity = %s WHERE id = %s;", (new_qty, order_id))
    conn.commit()
    cur.close()
    release_db_connection(conn)
    return jsonify({"message": "Quantity updated"})

@app.route('/orders/bulk-deliver', methods=['PUT'])
def bulk_deliver():
    """
    6. BULK DELIVER (Extra Update)
    ---
    responses:
      200:
        description: Orders updated
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status = 'Delivered' WHERE status = 'Shipped';")
    count = cur.rowcount
    conn.commit()
    cur.close()
    release_db_connection(conn)
    return jsonify({"message": f"{count} orders updated"})

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """
    7. CANCEL ORDER (Delete)
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
    responses:
      200:
        description: Order deleted
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM orders WHERE id = %s;", (order_id,))
    conn.commit()
    cur.close()
    release_db_connection(conn)
    return jsonify({"message": "Order deleted"})

if __name__ == '__main__':
    app.run(debug=True)