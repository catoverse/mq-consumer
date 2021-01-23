import paho.mqtt.client as mqttClient
import time
import ssl
import mysql.connector.pooling
import json
from flask import Flask
from project import app


broker_address= app.config['MQ_BROKER_ADDRESS'] # No ssl://
port = app.config['MQ_PORT']
user = app.config['MQ_USER']
password = app.config['MQ_PASSWORD']
CLIENT_NAME = app.config['MQ_CLIENT_NAME']

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

def on_connect(client, userdata, flags, rc):        
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        #Connected = True                #Signal connection
        client.subscribe("user_information")
        client.subscribe("video_information")
    else:
        print("Connection failed")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    payload = json.loads(msg.payload)
    payload_table  = ''
    if(msg.topic == 'user_information'):
        payload_table = add_user_information
    else:
        payload_table = add_video_information
    cnx = cnxPool.get_connection()
    cursor = cnx.cursor()
    cursor.execute(payload_table, payload)
    cnx.commit()
    cursor.close()
    cnx.close()
    
    
def connect_to_db():
    return mysql.connector.pooling.MySQLConnectionPool(pool_name = "catoRawFeedPool", pool_size = 3, **mySqlConfig)

context = ssl.create_default_context()
Connected = False

client = mqttClient.Client(CLIENT_NAME) #create new instance
client.username_pw_set(user, password=password) #set username and password
client.on_connect=on_connect
client.on_message=on_message
client.tls_set_context(context=context)
client.connect(broker_address, port=int(port))
client.loop_start()

cnxPool = connect_to_db()

while True:
    time.sleep(1)