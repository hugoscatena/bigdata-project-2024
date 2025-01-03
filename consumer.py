from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'logs_machine',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda v: v.decode('utf-8')
)

print("En attente de messages sur logs_machine...")

for message in consumer:
    print(f"Message reçu : {message.value}")
