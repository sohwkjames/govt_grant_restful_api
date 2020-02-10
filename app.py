from flask import Flask, jsonify, request
import json
import sqlite3
import datetime
import urllib.request
app = Flask(__name__)

DB_NAME = 'households.db'

@app.route('/')
def displayWelcome():
    return "Welcome! Please refer to the readme to view all endpoints."

# GET, view all households, return a json. Endpoint 3.
@app.route('/household', methods=['GET'])
def viewHouseholds():
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
def viewSingleHousehold(household_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM member LEFT JOIN household on member.HouseholdID = household.HouseholdID WHERE member.HouseholdID = ?",
                (household_id,))
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall() # gets list of row values
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    cur.close()
    return jsonify(json_data)

# POST, create a new household. Endpoint 1.
@app.route('/household', methods=['POST'])
def addHousehold():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # Example of expected json: {"HouseholdType":"HDB"}
    incoming_json = request.get_json()
    cur.execute('INSERT INTO household(HouseholdType) VALUES (?)', (incoming_json['HouseholdType'],))
    conn.commit()
    cur.close()
    return jsonify(success=True)

# POST, create a member, add to household. Endpoint 2.
@app.route('/member', methods=['POST'])
def addMember():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    incoming_json = request.get_json()
    cur.execute('INSERT INTO member(HouseholdID, Name, YOB, MaritalStatus, Spouse, OccupationType, AnnualIncome, Gender) VALUES(?,?,?,?,?,?,?,?)',
                (incoming_json['HouseholdID'], incoming_json['Name'], incoming_json['YOB'],
                 incoming_json['MaritalStatus'], incoming_json['Spouse'], incoming_json['OccupationType'],
                 incoming_json['AnnualIncome'], incoming_json['Gender'])),
    conn.commit()
    cur.close()
    return jsonify(success=True)


# GET, Search for households and receipent of grand disbursement. Takes household size, income. Endpoint 5.
# Returns families and households that qualify for the grant, given the constraints of max household and max income.
@app.route('/grants/<int:maxHouseholdSize>/<int:maxHouseholdIncome>', methods=['GET'])
def viewGrants(maxHouseholdSize, maxHouseholdIncome):

    if maxHouseholdIncome == 0:
        maxHouseholdIncome = 2 ** 30
    if maxHouseholdSize == 0:
        maxHouseholdSize = 99

    allGrantResults = []
    allGrantResults.append(getYoloGstGrant(maxHouseholdSize, maxHouseholdIncome))
    allGrantResults.append(getBabySunshineGrant(maxHouseholdSize, maxHouseholdIncome))
    allGrantResults.append(getElderBonusGrant(maxHouseholdSize, maxHouseholdIncome))
    allGrantResults.append(getStudentEncouragementBonus(maxHouseholdSize, maxHouseholdIncome))
    allGrantResults.append(getFamilyTogetherness(maxHouseholdSize, maxHouseholdIncome))

    print("all Grant results", allGrantResults)
    return jsonify(allGrantResults)


def getYoloGstGrant(maxHouseholdSize, maxHouseholdIncome):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # Get YOLO GST Grant: HDB Households, sum annual income <= 100,000
    maxHouseholdIncome = min(maxHouseholdIncome, 100000)
    cur.execute('''SELECT household.HouseholdID, household.HouseholdType, SUM(AnnualIncome) FROM member
                LEFT JOIN household on member.HouseholdID = household.HouseholdID
                GROUP BY member.HouseholdID HAVING SUM(AnnualIncome) < (?)
                AND household.HouseholdType = "HDB" AND count(MemberID) <= (?)''', (maxHouseholdIncome, maxHouseholdSize))
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    cur.close()
    return {"Yolo GST Grant":json_data}
    return jsonify(allGrantResults)

def getBabySunshineGrant(maxHouseholdSize, maxHouseholdIncome):
    # Returns households and members who are younger than 5.
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    curr_year = datetime.datetime.now().year
    cur.execute('''SELECT *, (?) - YOB as Age FROM member WHERE Age < 5 AND HouseholdID IN
                    (SELECT HouseholdID FROM member GROUP BY HouseholdID HAVING sum(AnnualIncome) < (?)
                    AND count(MemberID) <= (?))''', (curr_year, maxHouseholdIncome, maxHouseholdSize))
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    cur.close()
    return {"Baby Sunshine Grant":json_data}

def getElderBonusGrant(maxHouseholdSize, maxHouseholdIncome):
    # Returns households and members who are younger than 5.
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    curr_year = datetime.datetime.now().year

    cur.execute('''SELECT *, (?) - YOB as Age FROM member WHERE Age > 50 AND HouseholdID IN
                    (SELECT HouseholdID FROM member GROUP BY HouseholdID HAVING sum(AnnualIncome) < (?)
                     AND count(MemberID) <= (?))''', (curr_year, maxHouseholdIncome, maxHouseholdSize))
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    cur.close()
    return {"Elder Bonus":json_data}

def getStudentEncouragementBonus(maxHouseholdSize, maxHouseholdIncome):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    curr_year = datetime.datetime.now().year

    cur.execute('''SELECT *, (?) - YOB as Age FROM member WHERE Age < 16 AND HouseholdID in
                    ( SELECT HouseholdID FROM member GROUP BY HouseholdID having sum(AnnualIncome) < (?)
                        AND count(MemberID) < (?))''', (curr_year,maxHouseholdIncome, maxHouseholdSize))

    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    cur.close()
    return {"Student Encouragement Bonus":json_data}

def getFamilyTogetherness(maxHouseholdSize, maxHouseholdIncome):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    curr_year = datetime.datetime.now().year

    cur.execute('''SELECT *, (?) - YOB as Age FROM member WHERE Age < 18 AND Spouse <> 0 AND HouseholdID in
                    ( SELECT HouseholdID FROM member GROUP BY HouseholdID having sum(AnnualIncome) < (?)
                        AND count(MemberID) < (?))''', (curr_year,maxHouseholdIncome, maxHouseholdSize))

    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    cur.close()
    return {"Family Togetherness Scheme":json_data}


app.run(port=5000, debug=True)


 #FROM member WHERE EXISTS
#(SELECT *, SUM(AnnualIncome) FROM member GROUP BY HouseholdID HAVING AnnualIncome < 5000)''', (curr_year,))
