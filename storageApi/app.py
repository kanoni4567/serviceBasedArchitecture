import connexion

from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import and_

from base import Base
from item import Item
from wishlistItem import WishlistItem
import datetime

DB_ENGINE = create_engine('sqlite:///items.sqlite')
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
                 .filter(and_(Item.date_created >= startDate, Item.date_created <= endDate)))
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
                 .filter(and_(WishlistItem.date_created >= startDate, WishlistItem.date_created <= endDate)))
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
