from flask import Flask, jsonify, render_template
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connect to the database
conn = pymysql.connect(host='localhost', user='root', password='Tharun@123', db='nunam')

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(port=8080)
