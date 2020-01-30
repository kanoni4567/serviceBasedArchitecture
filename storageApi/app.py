import connexion
import yaml

from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import and_

from base import Base
from item import Item
from wishlistItem import WishlistItem
import datetime

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    datastore = app_config['datastore']
    db_user = datastore['user']
    db_password = datastore['password']
    db_hostname = datastore['hostname']
    db_port = datastore['port']
    db_schema = datastore['db']




DB_ENGINE = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(db_user, db_password, db_hostname, db_port, db_schema))
# DB_ENGINE = create_engine('sqlite:///items.sqlite')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def add_item(item):
    """ Receives an item posting """

    session = DB_SESSION()

    bp = Item(item['sellerId'],
                       item['name'],
                       item['timestamp'],
                       item['description'],
                       item['status'],
                       item['price'])

    session.add(bp)

    session.commit()
    session.close()

    return NoContent, 201


def get_item(startDate=None, endDate=None):
    """ Get item posting from the data store """

    results_list = []

    session = DB_SESSION()

    if startDate is not None and endDate is not None:
        results = (session.query(Item)
                 .filter(and_(Item.date_created >= datetime.datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S"),
                              Item.date_created <= datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%S"))))
    else:
        results = session.query(Item).all()

    for result in results:
        results_list.append(result.to_dict())
        print(result.to_dict())

    session.close()

    return results_list, 200


def add_wishlistItem(wishlistItem):
    """ Add a wishlist item to the data store """

    session = DB_SESSION()

    hr = WishlistItem(wishlistItem['userId'],
                   wishlistItem['itemId'],
                   wishlistItem['notifyChanges'])

    session.add(hr)

    session.commit()
    session.close()


    return NoContent, 201


def get_wishlistItem(startDate=None, endDate=None):
    """ Get wish list item from the data store """

    results_list = []

    session = DB_SESSION()

    if startDate is not None and endDate is not None:
        results = (session.query(WishlistItem)
                 .filter(and_(WishlistItem.date_created >= datetime.datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S"),
                              WishlistItem.date_created <= datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%S"))))
    else:
        results = session.query(WishlistItem).all()

    for result in results:
        results_list.append(result.to_dict())

    session.close()

    return results_list, 200


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    # run our standalone gevent server
    app.run(port=8090)
