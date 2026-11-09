#!/usr/bin/env python3
import sys
from datetime import datetime

DIAS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

for linea in sys.stdin:
    linea = linea.strip()                      # quita \r\n
    if not linea or linea.startswith("id,"):   # ignora encabezado y vacías
        continue
    try:
        c = linea.split(",")
        if len(c) != 8:
            continue
        fecha = datetime.strptime(c[1], "%Y-%m-%d %H:%M:%S")
        cantidad = int(c[5])
        metodo = c[7]
        print(f"{metodo}|{DIAS[fecha.weekday()]}\t{cantidad}")
    except (ValueError, IndexError):
        continue                               # línea mal formada: se salta