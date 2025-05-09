from kafka import KafkaConsumer
import json
from elasticsearch import Elasticsearch

def consume_from_kafka():
    consumer = KafkaConsumer(
        'market-price-topic',  # Kafka에서 구독할 주제
        bootstrap_servers=['kafka:9092'],  # Kafka 브로커 주소
        group_id='my-group',
        auto_offset_reset='earliest',  # 가장 처음부터 메시지를 읽음
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    es = Elasticsearch(['http://elasticsearch:9200'])

    for message in consumer:
        data = message.value
        print(f"Received message: {data}")

        es.index(index='market-price-index', doc_type='_doc', body=data)
        print(f"Data indexed in Elasticsearch: {data}")
