import time
import subprocess
from kafka import KafkaConsumer

# Paramètres de consommation Kafka
consumer = KafkaConsumer(
    'logs_machine',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',    # ou 'latest' selon vos besoins
    enable_auto_commit=True
)

local_file = "temp_logs.txt"      # Fichier local qui accumule les logs
hdfs_target = "/user/kafka/logs/logs_machine.txt"

last_upload_time = time.time()
upload_interval = 60  # en secondes (toutes les 60 s, on pousse sur HDFS)

print("Démarrage du consumer Kafka -> HDFS...")
print("Lecture des messages sur 'logs_machine'...")

try:
    for message in consumer:
        # 1) Écrire immédiatement le message dans un fichier local
        with open(local_file, "a", encoding="utf-8") as f:
            f.write(message.value.decode("utf-8") + "\n")
        
        # 2) Vérifier si c'est le moment de pousser sur HDFS
        current_time = time.time()
        if current_time - last_upload_time >= upload_interval:
            # On transfère le contenu vers HDFS
            print(f"\n[{time.strftime('%H:%M:%S')}] Envoi des logs vers HDFS...")

            # Exemple avec -appendToFile :
            # Si la commande -appendToFile n'est pas dispo, utiliser -put ou -moveFromLocal
            subprocess.run([
                r"C:\hadoop\hadoop-3.3.6\bin\hdfs.cmd",
                "dfs",
                "-put",  # or '-moveFromLocal'
                "-f",    # (optional) to force overwriting if the file exists
                local_file,
                hdfs_target
            ])


            # On vide le fichier local
            open(local_file, "w").close()

            # On met à jour le timer
            last_upload_time = current_time

except KeyboardInterrupt:
    print("\nArrêt demandé par l'utilisateur.")
finally:
    consumer.close()
    print("Consumer arrêté.")
