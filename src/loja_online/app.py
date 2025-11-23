import os
from flask import Flask, jsonify

# Expor um app WSGI chamado `app` para gunicorn/render
app = Flask(__name__)


@app.route("/health")
def health():
    """Health check endpoint. Retorna 200 OK com um JSON simples."""
    return jsonify({"status": "ok"}), 200


def create_app():
    """Factory caso a aplicação precise ser criada programaticamente."""
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Em produção o servidor WSGI (gunicorn) deve ser usado; este é para dev.
    app.run(host="0.0.0.0", port=port, debug=False)
