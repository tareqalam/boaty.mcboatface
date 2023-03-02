import pymysql.cursors
import pymysql

def get_connection():
    # Connect to the database
    # TODO
    # read secret.txt
    # get the password
    # use the password here
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='1',
                                database='boatydb',
                                charset='utf8mb4',
                                port=33069,
                                cursorclass=pymysql.cursors.DictCursor)
    return connection