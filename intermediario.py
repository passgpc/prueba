from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/confirm', methods=['GET'])
def confirm():
    return jsonify({"confirmation": 78}), 200

@app.route('/', methods=['GET'])
def home():
    return "Servidor en Render activo.", 200

if __name__ == "__main__":
    # Obtener el puerto de la variable de entorno PORT o usar 5000 como valor predeterminado
    port = int(os.environ.get("PORT", 1978))
    print(f"Servidor en Render iniciado. Escuchando en puerto {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
