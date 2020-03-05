import mysql.connector

db_conn = mysql.connector.connect(host="44.233.114.160", user="root", password="password", database="events")
db_cursor = db_conn.cursor()

db_cursor.execute('''DROP TABLE IF EXISTS `item`''')
db_cursor.execute('''
    CREATE TABLE item
        (id INT NOT NULL AUTO_INCREMENT, 
        sellerId VARCHAR(250) NOT NULL,
        name VARCHAR(250) NOT NULL,
        description VARCHAR(250) NOT NULL,
        status VARCHAR(250) NOT NULL,
        price INTEGER NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        date_created VARCHAR(100) NOT NULL,
        CONSTRAINT item_pk PRIMARY KEY (id))
    ''')

db_cursor.execute('''DROP TABLE IF EXISTS `wishlist_item`''')
db_cursor.execute('''
    CREATE TABLE wishlist_item
        (id INT NOT NULL AUTO_INCREMENT,
        userId VARCHAR(250) NOT NULL,
        itemId VARCHAR(250) NOT NULL,
        notifyChanges BOOLEAN NOT NULL,
        date_created VARCHAR(100) NOT NULL,
        CONSTRAINT wishlist_item_pk PRIMARY KEY (id))
    ''')
db_conn.commit()
db_conn.close()