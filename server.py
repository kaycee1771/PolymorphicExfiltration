from flask import Flask, request
from encryption import SecureEncryption

app = Flask(__name__)
encryption = SecureEncryption()

@app.route('/upload', methods=['POST'])
def receive_https_data():
    encrypted_data = request.form.get('payload', '')

    print(f"🔐 Received Encrypted Data: {encrypted_data}")

    try:
        decrypted_data = encryption.decrypt(encrypted_data)
        print(f"📥 Decrypted Data via HTTPS: {decrypted_data}")
        return "Received", 200
    except Exception as e:
        print(f"❌ Decryption Failed: {e}")
        return "Decryption Error", 500

if __name__ == '__main__':
    print("🚀 Starting the Flask Server on port 8080...")
    app.run(host="0.0.0.0", port=8080, debug=True)
