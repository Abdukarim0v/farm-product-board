import os, json
from datetime import datetime
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
QUEUE_NAME = os.getenv("QUEUE_NAME", "order_events")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/health")
def health():
    try:
        r.ping()
        q = "ok"
    except Exception as e:
        q = f"fail: {e}"
    return {"status": "ok", "queue": q, "time": datetime.utcnow().isoformat()}

@app.post("/orders")
def create_order():
    data = request.get_json(force=True)

    item = {
        "orderId": data.get("orderId"),
        "product": data.get("product"),
        "qty": data.get("qty"),
        "buyer": data.get("buyer"),
        "to": data.get("to"),
        "createdAt": datetime.utcnow().isoformat()
    }

    if not item["orderId"] or not item["product"] or not item["to"]:
        return {"error": "orderId, product, to required"}, 400

    r.rpush(QUEUE_NAME, json.dumps(item))
    return jsonify({"status": "queued", "event": item}), 202

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
