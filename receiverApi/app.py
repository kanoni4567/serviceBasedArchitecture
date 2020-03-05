import datetime
import json
import logging
import logging.config
import connexion
import requests
import yaml
from connexion import NoContent
from flask_cors import CORS
from pykafka import KafkaClient

STORE_SERVICE_ITEM_URL = "http://44.233.114.160:8090/items"
STORE_SERVICE_WISHLIST_ITEM_URL = "http://44.233.114.160:8090/wishlistItems"
HEADERS = { "content-type": "application/json"}

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

client = KafkaClient(hosts=kafka_server + ':' + str(kafka_port))
topic = client.topics[kafka_topic]
producer = topic.get_sync_producer()

def addItem(body):
    msg = {"type": "item",
           "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    # response = requests.post(STORE_SERVICE_ITEM_URL, json=body, headers=HEADERS)
    logger.info('Added an item')
    return NoContent, 200

# def updateItem(body):
#     print(body)
#     return 'Successful!', 200

def addWishListItem(body):
    msg = {"type": "wishlistItem",
           "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info('Added a wishlist item')
    # response = requests.post(STORE_SERVICE_WISHLIST_ITEM_URL, json=body, headers=HEADERS)
    return NoContent, 200

# def updateWishlistItem(body):
#     print(body)
#     return 'Successful!', 200


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8080)