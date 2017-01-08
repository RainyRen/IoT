# *********************************************************************
# Version:     2016.09.06
# Author:      Archer Huang
# License:     MIT
# Description: Get Data From MCS
# *********************************************************************
# 
# 1. install paho-mqtt
#	 pip install paho-mqtt
# *********************************************************************

import paho.mqtt.client as mqtt

# sys.path.insert(0, '/usr/lib/python2.7/bridge/')
# from bridgeclient import BridgeClient as bridgeclient

deviceId = "DJRs0jHX"
deviceKey = "GLBhC0Rrpj6p2KEW"
MQTT_SERVER = "mqtt.mcs.mediatek.com"
MQTT_PORT = 1883
MQTT_ALIVE = 60

MQTT_TOPIC_ALL = "mcs/" + deviceId + "/" + deviceKey + "/+"
# MQTT_TOPIC1 = "mcs/" + deviceId + "/" + deviceKey + "/Notification"
# MQTT_TOPIC2 = "mcs/" + deviceId + "/" + deviceKey + "/LED"
# MQTT_TOPIC3 = "mcs/" + deviceId + "/" + deviceKey + "/Temperature"
# MQTT_TOPIC4 = "mcs/" + deviceId + "/" + deviceKey + "/Humidity"
# MQTT_TOPIC5 = "mcs/" + deviceId + "/" + deviceKey + "/Dust"

def on_connect(client, userdata, flags, rc):
    print("MQTT Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC_ALL)
    # client.subscribe(MQTT_TOPIC1)


def on_message(client, userdata, msg):
    # print("mqtt payload=%s" %(msg.payload))
    # mqtt payload=1481790904274,Notification,Hi
    message = msg.payload.split(",")
    
    print message
    commadClassify(message)

def commadClassify(dataString):
	commandType = dataString[1]

	# Check recied type
	if commandType == "Notification":
		notifiMessage = dataString[2]
		print notifiMessage

	# If received data is not message, it must be weather data
	elif commandType == "Humidity":
		humidity = dataString[2]
		temperature = dataString[5]
		dust = dataString[8]
		print temperature, " ", humidity, " ", dust 
    # print message[2]

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)
mqtt_client.loop_forever()