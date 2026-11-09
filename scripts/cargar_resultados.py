import os
import sys
import psycopg2

ruta = sys.argv[1] if len(sys.argv) > 1 else "/data/output/resultado/part-00000"

con = psycopg2.connect(
    host=os.environ.get("DB_HOST", "db"),
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
)
with con, con.cursor() as cur:
    cur.execute("""CREATE TABLE IF NOT EXISTS resultados (
        id SERIAL PRIMARY KEY,
        metodo_pago TEXT NOT NULL,
        dia TEXT NOT NULL,
        unidades BIGINT NOT NULL,
        UNIQUE (metodo_pago, dia))""")
    n = 0
    with open(ruta) as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            clave, total = linea.split("\t")
            metodo, dia = clave.split("|")
            cur.execute(
                """INSERT INTO resultados (metodo_pago, dia, unidades)
                   VALUES (%s, %s, %s)
                   ON CONFLICT (metodo_pago, dia) DO UPDATE SET unidades = EXCLUDED.unidades""",
                (metodo, dia, int(total)))
            n += 1
con.close()
print(f"Insertados/actualizados: {n} registros")
