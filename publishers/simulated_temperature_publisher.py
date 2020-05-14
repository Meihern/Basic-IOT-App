import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime


def on_connect(rc):
    if rc != 0:
        print("Unable to connect to MQTT Broker")
    else:
        print("Connected with MQTT Broker : %s" % MQTT_BROKER)


def on_disconnect():
    pass


def on_publish(client, user_data, mid):
    pass


def publish_to_topic(topic, message):
    mqttc.publish(topic, message)
    print("Published : %s on MQTT Topic %s" % (message, topic))


def get_temperature_value(temperature_value):
    if temperature_value <= 5:
        return "VERY COLD"
    elif temperature_value <= 15:
        return "COLD"
    elif temperature_value <= 25:
        return "WARM"
    elif temperature_value <= 35:
        return "HOT"
    else:
        return "VERY HOT"


def get_random_number():
    m = float(10)
    s_rm = 1 - (1 / m) ** 2
    return (1 - random.uniform(0, s_rm)) ** .5


def publish_sensor_values_to_mqtt():
    threading.Timer(2.0, publish_sensor_values_to_mqtt).start()
    global toggle
    if toggle == 0:
        temperature_value = float("{0:.2f}".format(random.uniform(10, 100) * get_random_number()))
        temperature_data = dict()
        temperature_data['sensor_id'] = "temperature_sensor1"
        temperature_data['date_time'] = datetime.today().strftime("%d-%b-%Y %H:%M:%S:%f")
        temperature_data['temperature'] = temperature_value
        temperature_data['temperature_level'] = get_temperature_value(temperature_value)
        temperature_json_data = json.dumps(temperature_data)
        print("Publishing temperature value : %s ..." % temperature_value)
        publish_to_topic(MQTT_TOPIC_TEMPERATURE, temperature_json_data)
        toggle = 1
    else:
        toggle = 0


if __name__ == '__main__':
    MQTT_BROKER = "mqtt.eclipse.org"
    MQTT_PORT = 1883
    KEEP_ALIVE_INTERVAL = 30
    MQTT_TOPIC_TEMPERATURE = "Home/BedRoom/DHT1/Temperature"
    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.on_publish = on_publish
    mqttc.connect(MQTT_BROKER, int(MQTT_PORT), int(KEEP_ALIVE_INTERVAL))
    toggle = 0
    publish_sensor_values_to_mqtt()
