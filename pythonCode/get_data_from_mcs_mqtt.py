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
MQTT_TOPIC = "mcs/" + deviceId + "/" + deviceKey + "/+"

def on_connect(client, userdata, flags, rc):
    print("MQTT Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    # print("mqtt payload=%s" %(msg.payload))
    # mqtt payload=1481790904274,Notification,Hi
    message = msg.payload.split(",")
    commadType = message[1]
    dataInfo = message[2]
    print message
    commadSend(commadType, dataInfo)

def commadSend(commadType, dataString):
	if commadType == "Notification":
		if dataString == "1":
			print "1"

		if dataString == "2":
			print "2"

    # print message[2]

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)
mqtt_client.loop_forever()