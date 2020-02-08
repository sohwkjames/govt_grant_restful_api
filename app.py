from flask import Flask, jsonify
import json
import sqlite3

app = Flask(__name__)

DB_NAME = 'households.db'

# GET, view all households, return a json.
@app.route('/household', methods=['GET'])
def view_households():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    query = ("SELECT * FROM household")
    cur.execute(query)
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall() # gets list of row values
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    cur.close()
    return jsonify({"stores":json_data})


# GET, list a specific household by household ID
@app.route('/household/<int:household_id>', methods=['GET'])
def view_single_household(household_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    print("Before execute")
    cur.execute("SELECT * FROM household WHERE id=?", (household_id,))
    print("After execute")
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall() # gets list of row values

    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    cur.close()
    return jsonify(json_data)


# POST, create a household


# POST, add member to a household.






app.run(port=5000, debug=True)
