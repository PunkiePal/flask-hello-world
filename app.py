import os
import time
from flask import Flask, jsonify, request

app = Flask(__name__)

class MockLib:
    @property
    def TIME(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")
lib = MockLib()

@app.route('/webhook', methods=['POST'])
def handle_gumroad_webhook():
    try:
        data = request.form
        buyer_email = data.get("email")
        product_name = data.get("product_name")
        
        price_cents = int(data.get("price", 0))
        price_paid = price_cents / 100 

        if price_paid >= 149:
            print(f"[{lib.TIME}] Corporate $149 order received from {buyer_email} for {product_name}!")
        else:
            print(f"[{lib.TIME}] Standard $29 order received from {buyer_email} for {product_name}!")
            
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"[{lib.TIME}] ERROR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

