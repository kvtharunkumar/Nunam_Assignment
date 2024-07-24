from flask import Flask, jsonify, render_template
import pymysql
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

conn = pymysql.connect(host='localhost', user='root', password='', db='nunam')
# Connect to the database
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='nunam',
        cursorclass=pymysql.cursors.DictCursor  # Use DictCursor to get dictionaries instead of tuples
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/5308')
def cell_5308():
    return render_template('cell_5308.html')

@app.route('/5329')
def cell_5329():
    return render_template('cell_5329.html')



@app.route('/api/soh/<int:cell_id>')
def get_soh(cell_id):
    with conn.cursor() as cur:
        cur.execute("SELECT discharge_capacity, nominal_capacity FROM soh_data WHERE cell_id = %s", (cell_id,))
        row = cur.fetchone()
        if row:
            soh = (row[0] / row[1]) * 100
        else:
            soh = 0
    return jsonify({'cell_id': cell_id, 'soh': soh})

@app.route('/api/soh/all')
def get_all_soh():
    cell_ids = [5308, 5329]
    results = []
    for cell_id in cell_ids:
        with conn.cursor() as cur:
            cur.execute("SELECT discharge_capacity, nominal_capacity FROM soh_data WHERE cell_id = %s", (cell_id,))
            row = cur.fetchone()
            if row:
                soh = (row[0] / row[1]) * 100
                results.append({'cell_id': cell_id, 'soh': soh})
            else:
                results.append({'cell_id': cell_id, 'soh': 0})
    return jsonify(results)

@app.route('/api/cell_data/<int:cell_id>')
def cell_data(cell_id):
    try:
        data = get_cell_data(cell_id)
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": "Unable to fetch data"}), 500

def get_cell_data(cell_id):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            query = "SELECT time, voltage, current, capacity, temperature FROM cell_data WHERE cell_id = %s"
            cur.execute(query, (cell_id,))
            rows = cur.fetchall()
        conn.close()
        return {
            "time": [row['time'] for row in rows],
            "voltage": [row['voltage'] for row in rows],
            "current": [row['current'] for row in rows],
            "capacity": [row['capacity'] for row in rows],
            "temperature": [row['temperature'] for row in rows]
        }
    except pymysql.MySQLError as e:
        print(f"MySQL Error: {e}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == '__main__':
    app.run(port=8080)
