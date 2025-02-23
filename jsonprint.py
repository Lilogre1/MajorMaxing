import sqlite3
import json

def db_to_json(db_path, output_file):
    #connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #query all tables in  database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    db_data = {}
    for table_name in tables:
        table_name = table_name[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        #get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        column_info = cursor.fetchall()
        column_names = [col[1] for col in column_info]

        table_data = [dict(zip(column_names, row)) for row in rows]
        db_data[table_name] = table_data

    json_data = json.dumps(db_data, indent=4)

    with open(output_file, 'w') as json_file:
        json_file.write(json_data)

    #close database connection
    conn.close()

    #return JSON data
    return json_data


db_path = 'university_courses.db'
output_file = 'output.json'
json_data = db_to_json(db_path, output_file)