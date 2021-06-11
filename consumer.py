import stomp
import time
import mysql.connector.pooling
import json
from project import app


mq_broker_address = app.config['MQ_BROKER_ADDRESS']  # No ssl://
mq_port = app.config['MQ_PORT']
mq_user = app.config['MQ_USER']
mq_password = app.config['MQ_PASSWORD']

mySqlConfig = {
    'user': app.config['DB_USER'],
    'password': app.config['DB_PASSWORD'],
    'host': app.config['DB_HOST'],
    'database': app.config['DB_DATABASE'],
    'port': app.config['DB_PORT'],
    'raise_on_warnings': True
}

add_user_information = ("INSERT INTO user_information "
                        "(user_id, activity, description, create_timestamp) "
                        "VALUES (%(user_id)s, %(activity)s, %(description)s, %(create_timestamp)s)")

add_video_information = ("INSERT INTO video_information "
                         "(user_id, video_id, activity, description, create_timestamp) "
                         "VALUES (%(user_id)s, %(video_id)s, %(activity)s, %(description)s, %(create_timestamp)s)")


def connect_to_db():
    return mysql.connector.pooling.MySQLConnectionPool(pool_name="catoRawFeedPool", pool_size=3, **mySqlConfig)


def connect_and_subscribe(destination, listener, id):
    conn = stomp.Connection([(mq_broker_address, mq_port)],
                            heartbeats=(4000, 4000))

    conn.set_listener('', listener())
    conn.connect(mq_user, mq_password, wait=True)
    conn.subscribe(destination=destination, id=id,
                   ack='auto')
    return conn


class UserEventsConsumer(stomp.ConnectionListener):
    def on_connected(self, frame):
        print("User Events queue Connected Successfully")

    def on_error(self, frame):
        print('Error: "%s"' % frame.body)

    def on_disconnected(self):
        print('/queue/user Disconnected, trying to reconnect')
        connect_and_subscribe("/queue/user", VideoEventsConsumer, 1)

    def on_message(self, frame):
        print("message received",frame.body)
        payload = json.loads(frame.body)
        payload_table = add_user_information
        cnx = cnxPool.get_connection()
        cursor = cnx.cursor()
        cursor.execute(payload_table, payload)
        cnx.commit()
        cursor.close()
        cnx.close()


class VideoEventsConsumer(stomp.ConnectionListener):
    def on_connected(self, frame):
        print("Video Events queue Connected Successfully")

    def on_error(self, frame):
        print('Error: "%s"' % frame.body)

    def on_disconnected(self):
        print('/queue/video Disconnected, trying to reconnect')
        connect_and_subscribe("/queue/video", VideoEventsConsumer, 2)

    def on_message(self, frame):
        print(frame.body)
        payload = json.loads(frame.body)
        payload_table = add_video_information

        cnx = cnxPool.get_connection()
        cursor = cnx.cursor()
        cursor.execute(payload_table, payload)
        cnx.commit()
        cursor.close()
        cnx.close()


cnxPool = connect_to_db()

userEventsConn = connect_and_subscribe("/queue/user", UserEventsConsumer, 1)
videoEventsConn = connect_and_subscribe("/queue/video", VideoEventsConsumer, 2)



while (userEventsConn.is_connected() and videoEventsConn.is_connected()):
    time.sleep(2)
