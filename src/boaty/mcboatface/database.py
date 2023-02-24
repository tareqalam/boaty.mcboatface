import pymysql.cursors
import pymysql

def get_connection():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='1',
                                database='boatydb',
                                charset='utf8mb4',
                                port=33069,
                                cursorclass=pymysql.cursors.DictCursor)
    return connection