import time
import random
import json
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name = "logs_machine"

def generate_log_line():
    """
    Génère une ligne de log simulée.
    """
    log_types = ["INFO", "WARN", "ERROR", "DEBUG"]
    machines = ["machineA", "machineB", "machineC"]
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "machine": random.choice(machines),
        "log_level": random.choice(log_types),
        "message": "Ceci est un log simulé pour démonstration."
    }

def main():
    print(f"Envoi des logs sur le topic '{topic_name}'...")
    try:
        while True:
            log = generate_log_line()
            producer.send(topic_name, log)
            # Ajustez la fréquence d'envoi selon vos besoins (ici ~100 msgs/s)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Arrêt du script demandé par l'utilisateur.")
    finally:
        producer.close()

if __name__ == "__main__":
    main()
