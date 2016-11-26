import sys
import time

sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient as bridgeclient
value = bridgeclient()

while True:
	h0 = value.get("h")
	t0 = value.get("t")
	d0 = value.get("d")
	print "Temp:" + t0 + "*C"
	print "Humi:" + h0 + "%"
	print "PM2.5:" + d0 
	time.sleep(1)