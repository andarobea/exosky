from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   
#cors = CORS(app, resources={r"/process": {"origins": "http://127.0.0.1:5000"}})

@app.route('/process', methods=['POST'])
def process_string():
    data = request.get_json()
    input_string = data.get('inputString', '')
    # Use the string as a variable in your logic
    processed_string = input_string.upper()  # Example: processing the string
    return jsonify({"result": processed_string})

@app.route('/', methods=['GET'])
def render():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
