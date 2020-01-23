import connexion
import requests
import yaml
import logging
import logging.config
import json
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from connexion import NoContent

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    datastore_file = app_config['datastore']['filename']

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

STORE_SERVICE_ITEM_URL = app_config['eventstore']['url'] + "/items"
STORE_SERVICE_WISHLIST_ITEM_URL = app_config['eventstore']['url'] + "/wishlistItems"
HEADERS = {"content-type": "application/json"}


def get_item_stats():
    logger.info("Start responding get request to /events/stats")
    try:
        with open(datastore_file) as json_data_file:
            current_stat = json.load(json_data_file)
        logger.debug('Responding wish current stats %s', current_stat)
        logger.info("Finished responding get request to /events/stats")
        return current_stat, 200
    except FileNotFoundError:
        logger.error("Statistic file does not exist.")
    return NoContent, 404


def populate_stats():
    """ Periodically update stats """
    logger.info("Start Periodic Processing")
    last_update_date = "2020-01-22T11:55:01"
    prev_num_item_postings = 0
    prev_num_wishlist_items = 0
    stats = dict()
    try:
        with open(datastore_file) as json_data_file:
            current_stat = json.load(json_data_file)
        last_update_date = current_stat['updated_timestamp']
        prev_num_item_postings = current_stat['num_item_postings']
        prev_num_wishlist_items = current_stat['num_wishlist_items']
    except FileNotFoundError:
        logger.warning("Statistic file not exist, creating a new file.")

    current_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    params = {'startDate': last_update_date, 'endDate': current_date}
    items_response = requests.get(STORE_SERVICE_ITEM_URL, headers=HEADERS, params=params)
    wishlist_items_response = requests.get(STORE_SERVICE_WISHLIST_ITEM_URL, headers=HEADERS, params=params)

    if items_response.status_code != 200:
        logger.error("Item store api responded with a non 200 status code %s", items_response.status_code)
        return
    if wishlist_items_response.status_code != 200:
        logger.error("Wishlist item store api responded with a non 200 status code %s", wishlist_items_response.status_code)
        return

    new_items = items_response.json()
    logger.info("%d new items added.", len(new_items))

    new_wishlist_items = wishlist_items_response.json()
    logger.info("%d new wishlist items added.", len(new_wishlist_items))

    num_item_postings = prev_num_item_postings + len(new_items)
    num_wishlist_items = prev_num_wishlist_items + len(new_wishlist_items)

    result_stats = {
        "num_item_postings": num_item_postings,
        "num_wishlist_items": num_wishlist_items,
        "updated_timestamp": current_date
    }
    logger.debug('Updated statistics: %s', result_stats)
    with open(datastore_file, 'w') as fp:
        json.dump(result_stats, fp)

    logger.info("Finished Periodic Processing")



def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    # run our standalone gevent server
    init_scheduler()
    app.run(port=8100, use_reloader=False)
