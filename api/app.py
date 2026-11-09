import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request

app = Flask(__name__)


def conectar():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


def ejecutar(sql, params=()):
    con = conectar()
    try:
        with con, con.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall() if cur.description else cur.rowcount
    finally:
        con.close()


def iniciar_tabla():
    for _ in range(20):
        try:
            ejecutar("""CREATE TABLE IF NOT EXISTS resultados (
                id SERIAL PRIMARY KEY,
                metodo_pago TEXT NOT NULL,
                dia TEXT NOT NULL,
                unidades BIGINT NOT NULL,
                UNIQUE (metodo_pago, dia))""")
            return
        except psycopg2.OperationalError:
            time.sleep(2)
    raise RuntimeError("No se pudo conectar a la base de datos")


@app.get("/resultados")
def listar():
    return jsonify(ejecutar("SELECT * FROM resultados ORDER BY metodo_pago, id"))


@app.get("/resultados/<metodo_pago>")
def por_metodo(metodo_pago):
    filas = ejecutar(
        "SELECT * FROM resultados WHERE metodo_pago = %s ORDER BY id", (metodo_pago,))
    if not filas:
        return jsonify({"error": "no encontrado"}), 404
    return jsonify(filas)


@app.post("/resultados")
def crear():
    d = request.get_json(force=True)
    try:
        fila = ejecutar(
            "INSERT INTO resultados (metodo_pago, dia, unidades) VALUES (%s, %s, %s) RETURNING *",
            (d["metodo_pago"], d["dia"], d["unidades"]))
    except psycopg2.errors.UniqueViolation:
        return jsonify({"error": "ya existe esa combinacion"}), 409
    except KeyError:
        return jsonify({"error": "faltan campos"}), 400
    return jsonify(fila[0]), 201


@app.put("/resultados/<int:rid>")
def actualizar(rid):
    d = request.get_json(force=True)
    fila = ejecutar(
        "UPDATE resultados SET unidades = %s WHERE id = %s RETURNING *",
        (d["unidades"], rid))
    if not fila:
        return jsonify({"error": "no encontrado"}), 404
    return jsonify(fila[0])


@app.delete("/resultados/<int:rid>")
def borrar(rid):
    if ejecutar("DELETE FROM resultados WHERE id = %s", (rid,)) == 0:
        return jsonify({"error": "no encontrado"}), 404
    return jsonify({"borrado": rid})


if __name__ == "__main__":
    iniciar_tabla()
    app.run(host="0.0.0.0", port=5000)
