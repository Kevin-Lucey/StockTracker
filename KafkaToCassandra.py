from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from confluent_kafka import Consumer, KafkaError
import time
import json

# Cassandra configuration
cassandra_cluster = Cluster(
    ['192.168.56.1'],  # Localhost (change if your IP is different)
    port=9042  # Default Cassandra port
)
session = cassandra_cluster.connect('stocktracker')

kafka_conf = {
    'bootstrap.servers': 'localhost:9093',
    'group.id': 'stockevent_group',
    'auto.offset.reset': 'earliest'
}

# Initialize Consumer
consumer = Consumer(kafka_conf)
consumer.subscribe(['stockevent'])

print("connected")

def write_to_cassandra(data):
    cql = """
        INSERT INTO Tracker (tickerName,openPrice,high,low,closePrice,volume,recommendationKey,fiftyDayAverage,trackTime)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    session.execute(cql, (data['tickerName'], data['Open'], data['High'], 
                           data['Low'], data['Close'], str(data['Volume']), 
                           data['recommendationStrategy'], data['fiftyDayAverage'], data['timestamp']))
    print("Wrote event to Cassandra - >", data)

flag = True
try:
    while flag:
        print('listening...')
        time.sleep(1)
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        data = json.loads(msg.value().decode('utf-8'))
        write_to_cassandra(data)
        

        

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
    cassandra_cluster.shutdown()
