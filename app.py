



from flask import Flask, request, jsonify
from flasgger import Swagger
from db_config import db_crud_query, execute_featch_query

app = Flask(__name__)

# Swagger Configuration
template = {
    "swagger": "2.0",
    "info": {
        "title": "Order Management API - Nidhi Chaudhary",
        "description": "Complete CRUD API with PostgreSQL Function",
        "version": "1.0.0"
    },
    "host": "172.20.12.51:8089",
    "basePath": "/",
    "schemes": ["http"]
}

swagger = Swagger(app, template=template)

# ============================================
# 1. VIEW ALL ORDERS (Read) - Uses DB Function
# ============================================
@app.route('/orders', methods=['GET'])
def get_orders():
    """
    Get all orders with total amount calculated by DB function
    ---
    tags:
      - Orders
    responses:
      200:
        description: List of all orders
    """
    # Query uses PostgreSQL function get_total_amount
    query = """
        SELECT id, customer_name, product_name, price, quantity, status,
               get_total_amount(price, quantity) as total_amount
        FROM orders 
        ORDER BY id ASC;
    """
    
    result = execute_featch_query(query)
    
    # Check if error occurred 
    if isinstance(result, tuple):  # Error response
        return result
    
    orders = []
    for r in result:
        orders.append({
            "id": r[0],
            "customer": r[1],
            "product": r[2],
            "price": float(r[3]),
            "qty": r[4],
            "status": r[5],
            "total_amount": float(r[6])
        })
    
    return jsonify(orders), 200

# ============================================
# 2. PLACE ORDER (Create)
# ============================================
@app.route('/orders', methods=['POST'])
def add_order():
    """
    Place a new order
    ---
    tags:
      - Orders
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - customer_name
            - product_name
            - price
            - quantity
          properties:
            customer_name:
              type: string
              example: "Nidhi Chaudhary"
            product_name:
              type: string
              example: "Laptop"
            price:
              type: number
              example: 50000
            quantity:
              type: integer
              example: 2
    responses:
      201:
        description: Order created successfully
    """
    data = request.get_json()
    
    # Build query with values directly )
    query = f"""
        INSERT INTO orders (customer_name, product_name, price, quantity, status) 
        VALUES ('{data['customer_name']}', '{data['product_name']}', {data['price']}, {data['quantity']}, 'Pending');
    """
    
    result = db_crud_query(query)
    
    # If error occurred
    if result:
        return result
    
    return jsonify({"status": "success", "message": "Order created successfully"}), 201

# ============================================
# 3. UPDATE ORDER STATUS (Update)
# ============================================
@app.route('/orders/status/<int:order_id>', methods=['PUT'])
def update_status(order_id):
    """
    Update order status
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            status:
              type: string
              example: "Shipped"
    responses:
      200:
        description: Status updated successfully
    """
    data = request.get_json()
    
    query = f"UPDATE orders SET status = '{data['status']}' WHERE id = {order_id};"
    
    result = db_crud_query(query)
    
    if result:
        return result
    
    return jsonify({"status": "success", "message": "Status updated successfully"}), 200

# ============================================
# 4. CANCEL/DELETE ORDER (Delete)
# ============================================
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """
    Cancel/Delete an order
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Order deleted successfully
    """
    query = f"DELETE FROM orders WHERE id = {order_id};"
    
    result = db_crud_query(query)
    
    if result:
        return result
    
    return jsonify({"status": "success", "message": "Order deleted successfully"}), 200

# ============================================
# BONUS: Search Orders
# ============================================
@app.route('/orders/search', methods=['GET'])
def search_orders():
    """
    Search orders by customer name
    ---
    tags:
      - Orders
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
    
    query = f"SELECT * FROM orders WHERE customer_name ILIKE '%{name}%' ORDER BY id;"
    
    result = execute_featch_query(query)
    
    if isinstance(result, tuple):
        return result
    
    orders = [{"id": r[0], "customer": r[1], "product": r[2], "price": float(r[3]), "qty": r[4], "status": r[5]} for r in result]
    
    return jsonify(orders), 200

# EXACTLY AS YOU WANTS
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8089, debug=False, use_reloader=False)