from kafka import KafkaProducer
import json

def send_to_kafka(topic, message):
    producer = KafkaProducer(
        bootstrap_servers=['kafka:9092'],  # Kafka 브로커 주소
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # JSON 직렬화
    )
    producer.send(topic, message)
    producer.flush()
    print(f"Message sent to Kafka topic {topic}: {message}")
