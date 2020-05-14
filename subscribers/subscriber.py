import paho.mqtt.client as mqtt
import json, sqlite3


def on_connect(mosq, obj, rc):
    if rc == 0:
        print("connected")
        mqttc.subscribe(MQTT_Topic, 0)  # Subscribe to all Sensors at Base Topic
    else:
        print("bad connection")


def insert_data_into_table_query(table_name):
    if table_name == "humidity_data":
        insert_query = "insert into humidity_data(sensor_id, date_time, humidity, humidity_level) values (?, ?, ?, ?);"

    elif table_name == "temperature_data":
        insert_query = "insert into temperature_data(sensor_id, date_time, temperature, temperature_level) values (?, ?, ?, ?);"

    elif table_name == "acceleration_data":
        insert_query = "insert into acceleration_data(sensor_id, date_time, accX , accY, accZ) values (?, ?, ?, ?, ?);"

    else:
        return None

    return insert_query


def sensor_Data_Handler(topic: str, payload):
    db_table_name = topic.split('/').pop().lower() + '_data'
    print(db_table_name)
    data = json.loads(payload)
    insert_query = insert_data_into_table_query(db_table_name)
    try:
        conn = sqlite3.connect("Basic_Iot_DataBase.db")
        conn.execute(insert_query, tuple(data.values()))
        conn.commit()
    except Exception as e:
        print(e)


def on_message(mosq, obj, msg):
    # This is the Master Call for saving MQTT Data into DB
    try:
        print("MQTT Data Received...")
        print(msg.topic)
        print(msg.payload)
    except Exception as e:
        print(e)
    sensor_Data_Handler(msg.topic, msg.payload)  # Save Data into DB Table


def on_subscribe(mosq, obj, mid, granted_qos):
    pass


# MQTT Settings
if __name__ == '__main__':
    MQTT_Broker = "mqtt.eclipse.org"
    MQTT_Port = 1883
    Keep_Alive_Interval = 30
    MQTT_Topic = "Home/BedRoom/#"
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe
    # Connect & subscribe
    mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
    mqttc.subscribe(MQTT_Topic, 0)
    mqttc.loop_forever()  # Continue the network loop
