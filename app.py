from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ip_lookup', methods=['POST'])
def ip_lookup():
    if not request.is_json:
        return jsonify(status="error", message="Request must be JSON"), 400
    data = request.get_json(silent=True)
    if not data or "ip" not in data:
        return jsonify(status="error", message="IP is required"), 400
    ip = data["ip"]
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if res.status_code == 200:
            return jsonify(status="success", data=res.json())
        else:
            return jsonify(status="error", message="IP API failed", code=res.status_code), 502
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
