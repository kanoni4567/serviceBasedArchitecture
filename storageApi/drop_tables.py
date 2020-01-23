import sqlite3

conn = sqlite3.connect('items.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE item
          ''')
c.execute('''
          DROP TABLE wishlist_item
          ''')
conn.commit()
conn.close()
