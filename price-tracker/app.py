import os, sqlite3
from datetime import datetime
from flask import Flask, request, jsonify

DB_PATH = os.getenv("DB_PATH", "/data/price.db")

app = Flask(__name__)

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("""
      CREATE TABLE IF NOT EXISTS changes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT NOT NULL,
        old_price REAL NOT NULL,
        new_price REAL NOT NULL,
        changed_at TEXT NOT NULL
      )
    """)
    con.commit()
    con.close()

init_db()

@app.get("/health")
def health():
    return {"status":"ok","time":datetime.utcnow().isoformat()}

@app.post("/price-changes")
def add_change():
    data = request.get_json(force=True)
    product = data.get("product")
    old_price = data.get("oldPrice")
    new_price = data.get("newPrice")
    if not product or old_price is None or new_price is None:
        return {"error":"product, oldPrice, newPrice required"}, 400

    con = sqlite3.connect(DB_PATH)
    changed_at = datetime.utcnow().isoformat()
    con.execute(
      "INSERT INTO changes(product, old_price, new_price, changed_at) VALUES (?,?,?,?)",
      (product, float(old_price), float(new_price), changed_at)
    )
    con.commit()
    rowid = con.execute("SELECT last_insert_rowid()").fetchone()[0]
    con.close()

    return jsonify({"id": rowid, "product": product, "oldPrice": old_price, "newPrice": new_price, "changedAt": changed_at}), 201

@app.get("/price-changes")
def list_changes():
    con = sqlite3.connect(DB_PATH)
    rows = con.execute("SELECT id, product, old_price, new_price, changed_at FROM changes ORDER BY id DESC LIMIT 50").fetchall()
    con.close()
    return jsonify([
      {"id": r[0], "product": r[1], "oldPrice": r[2], "newPrice": r[3], "changedAt": r[4]} for r in rows
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
