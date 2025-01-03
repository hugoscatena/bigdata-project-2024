#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def run_mapper():
    """
    Fonction mapper: lit les lignes depuis stdin,
    émet "CLE\t1" selon le niveau de log repéré.
    """
    for line in sys.stdin:
        line = line.strip()
        # Par exemple, repérer 'INFO', 'WARN', 'ERROR' dans la ligne
        # (vérification simple, adapter selon ton format)
        if "INFO" in line:
            print("INFO\t1")
        elif "WARN" in line:
            print("WARN\t1")
        elif "ERROR" in line:
            print("ERROR\t1")
        else:
            print("OTHER\t1")


def run_reducer():
    """
    Fonction reducer: lit les paires "CLE\tVALEUR" depuis stdin,
    agrège les sommes par CLE, puis les affiche sur stdout.
    """
    current_key = None
    current_sum = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue  # ligne mal formée, on ignore

        key, val_str = parts
        val = int(val_str)

        if current_key == key:
            # Même clé => on cumule
            current_sum += val
        else:
            # Nouvelle clé => output du cumul précédent
            if current_key is not None:
                print(f"{current_key}\t{current_sum}")
            current_key = key
            current_sum = val

    # Gérer la dernière clé
    if current_key is not None:
        print(f"{current_key}\t{current_sum}")


if __name__ == "__main__":
    """
    On attend un argument: "mapper" ou "reducer"
    Par exemple:
      python log_mapreduce.py mapper
      python log_mapreduce.py reducer
    """
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: log_mapreduce.py [mapper|reducer]\n")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "mapper":
        run_mapper()
    elif mode == "reducer":
        run_reducer()
    else:
        sys.stderr.write(f"Mode inconnu: {mode}\n")
        sys.exit(1)
