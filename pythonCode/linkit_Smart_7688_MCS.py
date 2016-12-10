# *********************************************************************
# Version:     2016.09.06
# Author:      Archer Huang
# License:     MIT
# Description: Linkit Smart 7688 Duo + Arduino Code + Bridge + MCS
# *********************************************************************
# 
# 1. update opkg & disable bridge & install paho-mqtt
# 	 opkg update
# 	 uci set yunbridge.config.disabled=0
# 	 uci commit
#    pip install paho-mqtt
#    reboot
# *********************************************************************

import paho.mqtt.client as mqtt
import requests
import httplib, urllib
import time
import sys  
import json

sys.path.insert(0, '/usr/lib/python2.7/bridge/') 
from bridgeclient import BridgeClient as bridgeclient
value = bridgeclient()

# *********************************************************************
# MQTT Config

deviceId = "DJRs0jHX"
deviceKey = "GLBhC0Rrpj6p2KEW"
dataChnId1 = "Temperature"
dataChnId2 = "Humidity"
dataChnId3 = "Dust"
MQTT_SERVER = "mqtt.mcs.mediatek.com"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_TOPIC1 = "mcs/" + deviceId + "/" + deviceKey + "/" + dataChnId1
MQTT_TOPIC2 = "mcs/" + deviceId + "/" + deviceKey + "/" + dataChnId2
MQTT_TOPIC3 = "mcs/" + deviceId + "/" + deviceKey + "/" + dataChnId3

# *********************************************************************
# 25.018531, 121.536753
gps_alt=0
gps_lat=25.018531
gps_lon=121.536753
# *********************************************************************

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)	

# *********************************************************************
def post_to_mcs(payload):
    headers = {"Content-type": "application/json", "deviceKey": deviceKey}
    not_connected = 1
    while (not_connected):
        try:
            conn = httplib.HTTPConnection("api.mediatek.com:80")
            conn.connect()
            not_connected = 0
        except (httplib.HTTPException, socket.error) as ex:
            print "Error: %s" % ex
            time.sleep(10)  # sleep 10 seconds

    conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers)
    response = conn.getresponse()
    print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
    data = response.read()
    conn.close()
# *********************************************************************

while True:
    h0 = value.get("h")
    t0 = value.get("t")
    d0 = value.get("d")

    # value.put("alert", 123)

    payload = {"dataChnId":dataChnId1,"value":t0}
    print dataChnId1 + " : " + t0
    mqtt_client.publish(MQTT_TOPIC1, json.dumps(payload), qos=0)

    payload = {"dataChnId":dataChnId2,"value":h0}
    print dataChnId2 + " : " + h0
    mqtt_client.publish(MQTT_TOPIC2, json.dumps(payload), qos=0)

    payload = {"dataChnId":dataChnId3,"value":d0}
    print dataChnId3 + " : " + d0
    mqtt_client.publish(MQTT_TOPIC3, json.dumps(payload), qos=0)

    payload2 = {"datapoints":[{"dataChnId":"Humidity","values":{"value":h0}}, {"dataChnId":"Temperature","values":{"value":t0}}, {"dataChnId":"Dust","values":{"value":d0}}, {"dataChnId":"GPS","values":{"latitude":gps_lat, "longitude":gps_lon, "altitude": gps_alt}}]}
    post_to_mcs(payload2)
    
    time.sleep(10)