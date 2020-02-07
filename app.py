from flask import Flask, jsonify

app = Flask(__name__)


# Sample route to view all records in household db
@app.route('/household', methods=['GET'])
def view_households():
    return 0

app.run(port=5000, debug=True)
