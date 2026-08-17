import os
from flask import Flask, request, jsonify
from generate_pdf import create_manual

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def gumroad_webhook():
    if request.method == 'HEAD' or request.method == 'GET':
        return 'Server Live', 200
        
    try:
        data = request.form.to_dict()
        print("Received Gumroad Data:", data)
        
        customer_name = data.get('buyer_name', 'Individual Developer')
        license_key = data.get('license_key', 'INTERNAL-DEV-TEST')
        filename = f"manual_{license_key}.pdf"
        
        create_manual(filename, customer_name=customer_name, license_key=license_key)
        return jsonify({"status": "success", "file_created": filename}), 200
        
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5888))
    app.run(host='0.0.0.0', port=port)
