import datetime
import json

import connexion
import requests
import yaml
from connexion import NoContent
from pykafka import KafkaClient

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    kafka_conf = app_config['kafka']
    kafka_server = kafka_conf['server']
    kafka_port = kafka_conf['port']
    kafka_topic = kafka_conf['topic']

client = KafkaClient(hosts=kafka_server + ':' + str(kafka_port))
topic = client.topics[kafka_topic]

def get_item_by_offset(offset):
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=100)
    i = 0;
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == 'item':
            if i == offset:
                return msg['payload'], 200
            i += 1
    return NoContent, 400

def get_wishlistItem_by_offset(offset):
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, fetch_wait_max_ms=100)
    i = 0;
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == 'wishlistItem':
            if i == offset:
                return msg['payload'], 200
            i += 1
    return NoContent, 400


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8110)