import mysql.connector
db_conn = mysql.connector.connect(host="44.233.114.160", user="root", password="password", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''DROP TABLE IF EXISTS `item`''')
db_cursor.execute('''DROP TABLE IF EXISTS `wishlist_item`''')
db_conn.commit()
db_conn.close()