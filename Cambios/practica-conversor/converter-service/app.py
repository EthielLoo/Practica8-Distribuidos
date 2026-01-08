from flask import Flask, jsonify, request
import os, requests

app = Flask(__name__)

RATES_URL = os.getenv("RATES_URL", "http://rates-service:5001")

@app.get("/health")
def health():
    return jsonify(status="ok", service="converter", rates_url=RATES_URL)

@app.get("/convert")
def convert():
    amount_str = request.args.get("amount") or ""
    from_cur = (request.args.get("from") or "").upper()
    to_cur = (request.args.get("to") or "").upper()

    try:
        amount = float(amount_str)
    except:
        return jsonify(error="amount inválido. Ej: 100", received=amount_str), 400

    # Pide el rate al otro microservicio
    r = requests.get(f"{RATES_URL}/rate", params={"from": from_cur, "to": to_cur}, timeout=3)
    if r.status_code != 200:
        return jsonify(error="No se pudo obtener rate", details=r.json()), 400

    rate = r.json()["rate"]
    converted = round(amount * rate, 2)

    return jsonify(
        amount=amount,
        from_=from_cur,
        to=to_cur,
        rate=rate,
        converted=converted
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
