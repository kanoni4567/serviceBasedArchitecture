import datetime
import json
import logging.config

import connexion
import requests
import yaml
from connexion import NoContent
from flask_cors import CORS
from pykafka import KafkaClient
import os.path

if os.path.isfile('/config/app_conf.yml'):
    print('external conf found, using it')
    with open('/config/app_conf.yml', 'r') as f:
        app_config = yaml.safe_load(f.read())
        kafka_conf = app_config['kafka']
        kafka_server = kafka_conf['server']
        kafka_port = kafka_conf['port']
        kafka_topic = kafka_conf['topic']
else:
    print('external conf not found, using local conf')
    with open('app_conf.yml', 'r') as f:
        app_config = yaml.safe_load(f.read())
        kafka_conf = app_config['kafka']
        kafka_server = kafka_conf['server']
        kafka_port = kafka_conf['port']
        kafka_topic = kafka_conf['topic']



with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')




def get_item_by_offset(offset):
    client = KafkaClient(hosts=kafka_server + ':' + str(kafka_port))
    topic = client.topics[kafka_topic]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=100)
    i = 0;
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == 'item':
            if i == offset:
                consumer.stop()
                logger.info('Got the %d th item', offset)
                return msg['payload'], 200
            i += 1
    consumer.stop()
    logger.error('Could not find %d th item', offset)
    return NoContent, 400

def get_wishlistItem_by_offset(offset):
    client = KafkaClient(hosts=kafka_server + ':' + str(kafka_port))
    topic = client.topics[kafka_topic]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, fetch_wait_max_ms=100)
    i = 0;
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == 'wishlistItem':
            if i == offset:
                consumer.stop()
                logger.info('Got the %d th wishlist item', offset)
                return msg['payload'], 200
            i += 1
    consumer.stop()
    logger.error('Could not find %d th wishlist item', offset)
    return NoContent, 400


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8110)