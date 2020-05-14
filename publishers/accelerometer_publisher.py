import json
import re
import socket
import traceback
from datetime import datetime
from time import sleep

import paho.mqtt.client as mqtt
from pynput import keyboard


def on_press(key):
    global break_program
    print(key)
    if key == keyboard.Key.backspace:
        print('end pressed')
        break_program = True
        return False


def map_msg_to_json(msg, addr):
    dic = dict()
    lst = re.split("[,\"]", str(msg))
    dic['sensor_id'] = "Accelerometer %s" + str(addr)
    dic['date'] = datetime.today().strftime("%d-%b-%Y %H:%M:%S:%f")
    dic['accX'] = lst[2].strip()
    dic['accY'] = lst[3].strip()
    dic['accZ'] = lst[4].strip()
    return json.dumps(dic)


def on_connect(client, user_data, rc):
    if rc != 0:
        print("Unable to connect to MQTT Broker ...")
    else:
        print("Connected with MQTT Broker: %s" % MQTT_BROKER)


def on_publish(client, user_data, mid):
    pass


def on_disconnect(client, user_data, rc):
    if rc != 0:
        pass


def publish_to_topic(topic, message):
    mqttc.publish(topic, message)
    print("Published: %s on MQTT topic: %s" % (message, topic))


if __name__ == '__main__':
    MQTT_BROKER = "mqtt.eclipse.org"
    MQTT_PORT = 1883
    KEEP_ALIVE_INTERVAL = 30
    MQTT_TOPIC_ACCELERATION = "/Home/BedRoom/DHT1/Acceleration"
    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.on_publish = on_publish
    mqttc.connect(MQTT_BROKER, int(MQTT_PORT), int(KEEP_ALIVE_INTERVAL))
    break_program = False
    host = ""
    port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind((host, port))
    with keyboard.Listener(on_press=on_press) as listener:
        while break_program is False:
            try:
                print("gonna be detecting phone movement...")
                message, address = s.recvfrom(8192)
                acceleration_json_data = map_msg_to_json(message, address)
                publish_to_topic(MQTT_TOPIC_ACCELERATION, acceleration_json_data)
                sleep(1)
            except Exception as e:
                print("error")
                traceback.print_exc(e)
        listener.join()
