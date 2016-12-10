# **************************************************************************************************************************
# Version:     2016.06.30 
# Author:      Archer Huang
# License:     MIT
# Description: Linkit Smart 7688 Duo + Arduino Code + Bridge + AWS
# **************************************************************************************************************************
# 
# 1. update opkg & install wget & disable bridge
# 	 opkg update
# 	 uci set yunbridge.config.disabled=0
# 	 uci commit
#
# **************************************************************************************************************************

import time
import sys  
import datetime
import paho.mqtt.client as paho
import ssl
import os
import json

sys.path.insert(0, '/usr/lib/python2.7/bridge/') 
from bridgeclient import BridgeClient as bridgeclient
value = bridgeclient()

connflag = False

def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

awshost = "a2r87wwkzvbgnn.iot.ap-northeast-1.amazonaws.com"
awsport = 8883
clientId = "sensingData"
thingName = "get_things"
caPath = "/root/root-CA.crt"
certPath = "/root/get_things.cert.pem"
keyPath = "/root/get_things.private.key"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
mqttc.connect(awshost, awsport, keepalive=60)
mqttc.loop_start()

while True:
	humidity = value.get("h")
	temperature = value.get("t")
	dust = value.get("d")
	print "humidity: %d, temperature: %d" % (float(humidity), float(temperature))
	t = time.time();
	date = datetime.datetime.fromtimestamp(t).strftime('%Y%m%d%H%M%S')
	if connflag == True:
		mqttc.publish("topic/sensingData", json.dumps({"time": date, "temperature": temperature, "humidity": humidity}), qos=1)
	else:
		print("waiting for connection...")
	time.sleep(10)