📦 Order Management API
Developer: Nidhi Chaudhary

Module: Backend Order System with PostgreSQL Integration

📝 Project Description
This project is a RESTful API built with Flask to manage customer orders. It demonstrates full CRUD functionality and integrates advanced PostgreSQL Functions to handle business logic (like tax and discounts) directly in the database for better performance.

🚀 Key Features
🔹 Advanced CRUD Operations
Create & Read: Place new orders and view the entire order list.

Search Filter: A specialized GET route to find orders by Customer Name.

Smart Updates: Change order Status or update Quantity (which triggers bill recalculation).

Bulk Action: A "Bulk Deliver" feature to update multiple orders at once.

Conditional Delete: Orders can be canceled only if they haven't been shipped yet.

🔹 Database Functions (PL/pgSQL)
The system uses 6 custom DB functions to automate calculations:

get_total_amount: Base price × Quantity.

calculate_order_tax: Applies 18% GST.

get_discounted_total: Applies a 10% discount for bulk orders.

check_cancel_eligibility: Prevents deletion of shipped orders.

get_order_count_by_status: Provides quick stats for the dashboard.

get_shipping_label: Formats data for logistics labels.

🛠️ Technical Stack
Language: Python 3.x

Framework: Flask

Database: PostgreSQL (using psycopg2 connection pooling)

API Docs: Swagger (Flasgger)

⚙️ How to Run
Install Dependencies: pip install flask psycopg2-binary flasgger

Database: Run your SQL scripts in pgAdmin to create the orders table and the 6 functions.

Start Server: python app.py

Interactive Docs: Open http://127.0.0.1:5000/apidocs to test the API.