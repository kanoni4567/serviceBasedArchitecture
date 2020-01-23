from sqlalchemy import Column, Integer, String, DateTime, Boolean
from base import Base
import datetime


class WishlistItem(Base):
    """ Item Posting """

    __tablename__ = "wishlist_item"

    id = Column(Integer, primary_key=True)
    userId = Column(String(250), nullable=False)
    itemId = Column(String(250), nullable=False)
    notifyChanges = Column(Boolean, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, userId, itemId, notifyChanges):
        """ Initializes an item posting """
        self.userId = userId
        self.itemId = itemId
        self.notifyChanges = notifyChanges
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['userId'] = self.userId
        dict['itemId'] = self.itemId
        dict['notifyChanges'] = self.notifyChanges

        return dict
