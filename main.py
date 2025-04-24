from flask import Flask, jsonify
from compliance import run_compliance

app = Flask(__name__)

@app.route('/run', methods=['GET'])
def run():
    success = run_compliance()
    return jsonify({'status': 'success' if success else 'failure'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
