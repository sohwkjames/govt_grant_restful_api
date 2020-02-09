from flask import Flask, jsonify, request
import json
import sqlite3

app = Flask(__name__)

DB_NAME = 'households.db'

# GET, view all households, return a json. Endpoint 3.
@app.route('/household', methods=['GET'])
def view_households():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    query = ("SELECT * FROM member LEFT JOIN household on member.HouseholdID = household.HouseholdID")
    cur.execute(query)
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall() # gets list of row values
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    cur.close()
    return jsonify({"households":json_data})

# GET, list a specific household by household ID, returns a json. Endpoint 4.
@app.route('/household/<int:household_id>', methods=['GET'])
def view_single_household(household_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    print("Before execute")
    cur.execute("SELECT * FROM member LEFT JOIN household on member.HouseholdID = household.HouseholdID WHERE member.HouseholdID = ?",
                (household_id,))
    print("After execute")
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall() # gets list of row values
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    cur.close()
    return jsonify(json_data)

# POST, create a new household. Endpoint 1.
@app.route('/household', methods=['POST'])
def add_household():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # Example of expected json: {"HouseholdType":"HDB"}
    incoming_json = request.get_json()
    print(incoming_json['HouseholdType'])
    cur.execute('INSERT INTO household(HouseholdType) VALUES (?)', (incoming_json['HouseholdType'],))
    conn.commit()
    cur.close()
    return jsonify(success=True)

# POST, create a member, add to household. Endpoint 2.
@app.route('/member', methods=['POST'])
def add_member():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    incoming_json = request.get_json()
    print("Before execute")
    cur.execute('INSERT INTO member(HouseholdID, Name, YOB, MaritalStatus, Spouse, OccupationType, AnnualIncome, Gender) VALUES(?,?,?,?,?,?,?,?)',
                (incoming_json['HouseholdID'], incoming_json['Name'], incoming_json['YOB'],
                 incoming_json['MaritalStatus'], incoming_json['Spouse'], incoming_json['OccupationType'],
                 incoming_json['AnnualIncome'], incoming_json['Gender'])),
    conn.commit()
    cur.close()
    return jsonify(success=True)






app.run(port=5000, debug=True)
