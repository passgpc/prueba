from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/confirm', methods=['GET'])
def confirm():
    # Responder siempre con el número 78
    return jsonify({"confirmation": 78}), 200

if __name__ == "__main__":
    print("Servidor en Render iniciado. Escuchando en /confirm...")
    app.run(host='0.0.0.0', port=1978)
