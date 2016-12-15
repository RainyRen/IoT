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
dataChnId4 = "GPS"
getChnId1 = "LED"
MQTT_SERVER = "mqtt.mcs.mediatek.com"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_TOPIC1 = "mcs/" + deviceId + "/" + deviceKey + "/" + dataChnId1
MQTT_TOPIC2 = "mcs/" + deviceId + "/" + deviceKey + "/" + dataChnId2
MQTT_TOPIC3 = "mcs/" + deviceId + "/" + deviceKey + "/" + dataChnId3

MQTT_TOPIC_MONITOR = "mcs/" + deviceId + "/" + deviceKey + "/" + getChnId1
# *********************************************************************
# 25.018531, 121.536753
gps_alt = 0
gps_lat = 25.018531
gps_lon = 121.536753
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
    #print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
    print response.status
    data = response.read()
    conn.close()
# *********************************************************************
# Get data from MQTT Server
def on_connect(client, userdata, flags, rc):
    print("MQTT Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC_MONITOR)

def on_message(client, userdata, msg):
    print("mqtt payload=%s" %(msg.payload))
# *********************************************************************
def establishCommandChannel():
    # Query command server's IP & port
    connectionAPI = 'https://api.mediatek.com/mcs/v2/devices/%(device_id)s/connections.csv'
    r = requests.get(connectionAPI % DEVICE_INFO,
                 headers = {'deviceKey' : DEVICE_INFO['device_key'],
                            'Content-Type' : 'text/csv'})
    logging.info("Command Channel IP,port=" + r.text)
    (ip, port) = r.text.split(',')

    # Connect to command server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, int(port)))
    s.settimeout(None)
# ************************************************************************
# mqtt_client.loop_start()

while True:
    h0 = value.get("h")
    t0 = value.get("t")
    d0 = value.get("d")

    # value.put("alert", 123)
# ***********************************************************************
    # MQTT clint publish data
    payload = {"dataChnId":dataChnId1,"value":t0}
    #print dataChnId1 + " : " + t0
    mqtt_client.publish(MQTT_TOPIC1, json.dumps(payload), qos=0)

    payload = {"dataChnId":dataChnId2,"value":h0}
    #print dataChnId2 + " : " + h0
    mqtt_client.publish(MQTT_TOPIC2, json.dumps(payload), qos=0)

    payload = {"dataChnId":dataChnId3,"value":d0}
    #print dataChnId3 + " : " + d0
    mqtt_client.publish(MQTT_TOPIC3, json.dumps(payload), qos=0)

    payload = {"dataChnId":dataChnId4,"value":{"latitude":gps_lat, "longitude":gps_lon, "altitude": gps_alt}}
    #print dataChnId4 + " : latitude = {LA} | longitude = {LO} | altitude = {AL}".format(LA=gps_lat, LO=gps_lon, AL=gps_alt)
    mqtt_client.publish(MQTT_TOPIC3, json.dumps(payload), qos=0)
# ************************************************************************
    #  Http clint send data
    payload2 = {"datapoints":[{"dataChnId":dataChnId2,"values":{"value":h0}}, {"dataChnId":dataChnId1,"values":{"value":t0}}, {"dataChnId":dataChnId3,"values":{"value":d0}}, {"dataChnId":dataChnId4,"values":{"latitude":gps_lat, "longitude":gps_lon, "altitude": gps_alt}}]}
    post_to_mcs(payload2)
# ************************************************************************
    # mqtt_client.on_connect = on_connect
    # mqtt_client.on_message = on_message
    # mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)

    time.sleep(10)