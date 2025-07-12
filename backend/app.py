from flask import Flask, jsonify, send_from_directory
import os
import sqlite3

app = Flask(__name__, static_folder='static/vue', static_url_path='/static/vue')

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'adventureworks.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row # This allows accessing columns by name
    return conn

@app.route('/api/data')
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Fetching all products for this example
    cursor.execute("SELECT ProductID, Name, ListPrice, Color, Size FROM Product")
    products = cursor.fetchall()
    conn.close()

    # Convert list of Row objects to list of dicts
    products_list = [dict(row) for row in products]
    return jsonify(products_list)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue_app(path):
    vue_app_static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'vue')
    if path != "" and os.path.exists(os.path.join(vue_app_static_folder, path)):
        return send_from_directory(vue_app_static_folder, path)
    else:
        return send_from_directory(vue_app_static_folder, 'index.html')

if __name__ == '__main__':
    # Ensure the database exists before running the app
    if not os.path.exists(DATABASE_PATH):
        print(f"Database not found at {DATABASE_PATH}. Please run database_setup.py first.")
        # Optionally, you could try to run it here:
        # import database_setup
        # database_setup.create_database()
    app.run(debug=True, port=5000)
