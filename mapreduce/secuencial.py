#!/usr/bin/env python3
import sys
from collections import defaultdict
from datetime import datetime

DIAS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
acum = defaultdict(int)

with open(sys.argv[1]) as f:
    next(f)  # encabezado
    for linea in f:
        c = linea.strip().split(",")
        if len(c) != 8:
            continue
        try:
            d = datetime.strptime(c[1], "%Y-%m-%d %H:%M:%S").weekday()
            acum[f"{c[7]}|{DIAS[d]}"] += int(c[5])
        except ValueError:
            continue

for k in sorted(acum):
    print(f"{k}\t{acum[k]}")