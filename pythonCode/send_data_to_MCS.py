import requests
import httplib, urllib
import time
import sys
import json

deviceId = "DJRs0jHX"
deviceKey = "GLBhC0Rrpj6p2KEW"

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
    # print response.status
    data = response.read()
    conn.close()
# *********************************************************************
# Get data from MQTT Server
def on_connect(client, userdata, flags, rc):
    print("MQTT Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC_MONITOR)

def on_message(client, userdata, msg):
    #print("mqtt payload=%s" %(msg.payload))
    message = msg.payload.split(",")
    commadType = message[1]
    dataInfo = message[2]
    print message


while True:

	payload2 = {"datapoints":[{"dataChnId":"EmergencyNumber","values":{"value":"0"}}, {"dataChnId":"Emergency","values":{"value":"0"}}]}
	post_to_mcs(payload2)

	time.sleep(10)