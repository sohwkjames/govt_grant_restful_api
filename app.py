from flask import Flask

app = Flask(__name__)

@app.route('/family', methods=['GET'])
def createFamily():
    return "Hello"

app.run(port=5000, debug=True)
