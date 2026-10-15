import os
from flask import Flask, request, jsonify, render_template_string
from google import genai

app = Flask(__name__)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jarvis - Asistente IA</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; max-width: 600px; margin: 20px auto; padding: 15px; box-sizing: border-box; }
        h1 { font-size: 1.5rem; text-align: center; margin-bottom: 15px; }
        .chat-box { background: #1e293b; border-radius: 12px; padding: 15px; height: 65vh; overflow-y: auto; margin-bottom: 15px; display: flex; flex-direction: column; gap: 10px; }
        .message { padding: 10px 14px; border-radius: 8px; max-width: 85%; line-height: 1.4; word-break: break-word; }
        .user { background: #3b82f6; align-self: flex-end; }
        .jarvis { background: #334155; align-self: flex-start; }
        .input-box { display: flex; gap: 10px; }
        input { flex: 1; padding: 12px; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: white; font-size: 16px; outline: none; }
        button { padding: 12px 20px; border-radius: 8px; border: none; background: #3b82f6; color: white; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Jarvis AI</h1>
    <div class="chat-box" id="chatBox">
        <div class="message jarvis">¡Hola! Soy Jarvis. ¿En qué te puedo ayudar hoy?</div>
    </div>
    <div class="input-box">
        <input type="text" id="userInput" placeholder="Escribe un mensaje..." onkeypress="if(event.key === 'Enter') sendMessage()">
        <button onclick="sendMessage()">Enviar</button>
    </div>
    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const chatBox = document.getElementById('chatBox');
            const text = input.value.trim();
            if (!text) return;

            chatBox.innerHTML += `<div class="message user">${text}</div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({mensaje: text})
                });
                const data = await res.json();
                const reply = data.respuesta || data.error || 'Error de respuesta';
                chatBox.innerHTML += `<div class="message jarvis">${reply}</div>`;
            } catch (err) {
                chatBox.innerHTML += `<div class="message jarvis">Error de conexión con el servidor.</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE), 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("mensaje", "")
    
    if not user_message:
        return jsonify({"error": "No se proporcionó ningún mensaje."}), 400

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_message,
        )
        return jsonify({"respuesta": response.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
