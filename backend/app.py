import os
import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", "/data/products.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            qty INTEGER NOT NULL CHECK(qty >= 0),
            price REAL NOT NULL CHECK(price >= 0),
            updatedAt TEXT NOT NULL
        )
        """)
        conn.commit()

@app.get("/health")
def health():
    # DB ham ishlayotganini tekshiramiz (real monitoringga yaqin)
    try:
        with get_conn() as conn:
            conn.execute("SELECT 1")
        db = "ok"
    except Exception as e:
        db = f"fail: {e}"
    return {"status": "ok", "db": db, "time": datetime.utcnow().isoformat()}

@app.get("/products")
def list_products():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])

@app.post("/products")
def add_product():
    data = request.get_json(force=True)

    name = (data.get("name") or "").strip()
    qty = data.get("qty")
    price = data.get("price")

    # Basic validation (real app)
    if not name:
        return {"error": "name required"}, 400
    try:
        qty = int(qty)
        price = float(price)
    except Exception:
        return {"error": "qty must be int, price must be number"}, 400
    if qty < 0 or price < 0:
        return {"error": "qty and price must be >= 0"}, 400

    updated_at = datetime.utcnow().isoformat()

    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO products(name, qty, price, updatedAt) VALUES (?,?,?,?)",
            (name, qty, price, updated_at),
        )
        conn.commit()
        new_id = cur.lastrowid

    return {"id": new_id, "name": name, "qty": qty, "price": price, "updatedAt": updated_at}, 201

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
