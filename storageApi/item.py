from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Item(Base):
    """ Item Posting """

    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    sellerId = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    price = Column(Integer, nullable=False)

    def __init__(self, sellerId, name, timestamp, description, status, price):
        """ Initializes an item posting """
        self.sellerId = sellerId
        self.name = name
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()
        self.description = description
        self.status = status
        self.price = price

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['sellerId'] = self.sellerId
        dict['name'] = self.name
        dict['description'] = self.description
        dict['status'] = self.status
        dict['price'] = self.price
        dict['timestamp'] = self.timestamp

        return dict
