import sqlite3

conn = sqlite3.connect('items.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE item
          (id INTEGER PRIMARY KEY ASC, 
           sellerId VARCHAR(250) NOT NULL,
           name VARCHAR(250) NOT NULL,
           description VARCHAR(250) NOT NULL,
           status VARCHAR(250) NOT NULL,
           price INTEGER NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE wishlist_item
          (id INTEGER PRIMARY KEY ASC,
           userId VARCHAR(250) NOT NULL,
           itemId VARCHAR(250) NOT NULL,
           notifyChanges BOOLEAN NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
