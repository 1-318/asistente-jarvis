import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# Inicializamos el cliente de Gemini utilizando la variable de entorno segura
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return "¡Jarvis está en línea y funcionando perfectamente!", 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("mensaje", "")
    
    if not user_message:
        return jsonify({"error": "No se proporcionó ningún mensaje."}), 400

    try:
        # Generamos la respuesta usando el modelo más reciente y rápido de Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message,
        )
        return jsonify({"respuesta": response.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
  
