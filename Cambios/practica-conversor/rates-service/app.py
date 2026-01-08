from flask import Flask, jsonify, request

app = Flask(__name__)

# Tipos de cambio fijos (simple para práctica)
RATES = {
    ("USD", "MXN"): 17.20,
    ("EUR", "MXN"): 18.70,
    ("MXN", "USD"): 1/17.20,
    ("MXN", "EUR"): 1/18.70,
}

@app.get("/health")
def health():
    return jsonify(status="ok", service="rates")

@app.get("/rate")
def rate():
    from_cur = (request.args.get("from") or "").upper()
    to_cur = (request.args.get("to") or "").upper()

    key = (from_cur, to_cur)
    if key not in RATES:
        return jsonify(error="Rate no disponible", from_=from_cur, to=to_cur), 404

    return jsonify(from_=from_cur, to=to_cur, rate=RATES[key])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
