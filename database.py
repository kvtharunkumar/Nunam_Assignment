import pandas as pd
import mysql.connector

# DEFINE THE DATABASE CREDENTIALS
user = 'root'
password = 'Tharun@123'
host = '127.0.0.1'
database = 'nunam'

# Function to connect to the MySQL database
def get_connection():
    try:
        con = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print(f"Connection to the {host} for user {user} created successfully.")
        return con
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to create tables if they don't exist
def create_tables(con):
    cursor = con.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS soh_data (
        cell_id INT PRIMARY KEY,
        discharge_capacity FLOAT,
        nominal_capacity FLOAT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cell_data (
        cell_id INT,
        current FLOAT,
        voltage FLOAT,
        capacity FLOAT,
        temperature FLOAT,
        time FLOAT,
        FOREIGN KEY (cell_id) REFERENCES soh_data(cell_id)
    )
    """)
    con.commit()

# Function to insert SOH data
def insert_soh_data(con, soh_data):
    cursor = con.cursor()
    for _, row in soh_data.iterrows():
        cursor.execute("""
        INSERT INTO soh_data (cell_id, discharge_capacity, nominal_capacity)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        discharge_capacity = VALUES(discharge_capacity),
        nominal_capacity = VALUES(nominal_capacity)
        """, tuple(row))
    con.commit()

# Function to insert cell data
def insert_cell_data(con, cell_data, cell_id):
    cursor = con.cursor()
    for _, row in cell_data.iterrows():
        cursor.execute("""
        INSERT INTO cell_data (cell_id, current, voltage, capacity, temperature, time)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (cell_id, *row))
    con.commit()

if __name__ == '__main__':
    con = get_connection()
    if con:
        create_tables(con)

        # Load Excel files
        _5308_path = './ExcelSheets/5308.xls'
        _5329_path = './ExcelSheets/5329.xls'

        # Extract sheet names
        xls_5308 = pd.ExcelFile(_5308_path)
        xls_5329 = pd.ExcelFile(_5329_path)

        _5308_cols_sheet = xls_5308.sheet_names
        _5329_cols_sheet = xls_5329.sheet_names

        _5308_cols = {
            'Details': pd.read_excel(_5308_path, sheet_name=_5308_cols_sheet[3]),
            'Temp_detials': pd.read_excel(_5308_path, sheet_name=_5308_cols_sheet[-1])
        }
        _5329_cols = {
            'Details': pd.read_excel(_5329_path, sheet_name=_5329_cols_sheet[3]),
            'Temp_detials': pd.read_excel(_5329_path, sheet_name=_5329_cols_sheet[-1])
        }

        _5329_data = {
            'Current': _5329_cols['Details'].iloc[:, 5],
            'Voltage': _5329_cols['Details'].iloc[:, 6],
            'Capacity': _5329_cols['Details'].iloc[:, 7],
            'Temperature': _5329_cols['Temp_detials'].iloc[:, 4],
            'Time': _5329_cols['Details'].iloc[:, 10]
        }

        _5308_data = {
            'Current': _5308_cols['Details'].iloc[:, 5],
            'Voltage': _5308_cols['Details'].iloc[:, 6],
            'Capacity': _5308_cols['Details'].iloc[:, 7],
            'Temperature': _5308_cols['Temp_detials'].iloc[:, 4],
            'Time': _5308_cols['Details'].iloc[:, 10]
        }

        soh_data = pd.DataFrame({
            'cell_id': [5308, 5329],
            'discharge_capacity': [2992.02, 2822.56],
            'nominal_capacity': [3000, 3000]
        })

        # Insert data into MySQL
        insert_soh_data(con, soh_data)

        # Insert cell data
        data_5308_df = pd.DataFrame(_5308_data)
        insert_cell_data(con, data_5308_df, 5308)

        data_5329_df = pd.DataFrame(_5329_data)
        insert_cell_data(con, data_5329_df, 5329)

        con.close()
