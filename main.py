import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def gumroad_webhook():
    if request.method == 'HEAD' or request.method == 'GET':
        return 'Server Live', 200
        
    try:
        data = request.form.to_dict()
        print("Received Gumroad Data:", data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5888))
    app.run(host='0.0.0.0', port=port)
