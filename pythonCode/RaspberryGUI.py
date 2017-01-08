#-*- coding:utf-8 -*-  

from Tkinter import *
import time
import requests
import httplib, urllib
import json
import paho.mqtt.client as mqtt

deviceId = "DJRs0jHX"
deviceKey = "GLBhC0Rrpj6p2KEW"
MQTT_SERVER = "mqtt.mcs.mediatek.com"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_TOPIC_ALL = "mcs/" + deviceId + "/" + deviceKey + "/+"
dataChnId8 = "Emergency"
dataChnId9 = "EmergencyNumber"

classSchedule = {
					"Monday":['Chinese','Math','Math','English', 'Society','Science','Exercise'],
					"Tuesday":['Chinese','Math','Math','English', 'Society','Science','Exercise'],
					"Wednesday":['Chinese','Math','Math','English', 'Society','Science','Exercise'],
					"Thuesday":['Chinese','Math','Math','English', 'Society','Science','Exercise'],
					"Friday":['Chinese','Math','Math','English', 'Society','Science','Exercise']
				}

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
	# print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
	print response.status
	data = response.read()
	conn.close()

def on_connect(client, userdata, flags, rc):

	print("MQTT Connected with result code "+str(rc))
	client.subscribe(MQTT_TOPIC_ALL)

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

		checkWeatherState(temperature, humidity, dust)

def sendEmergence():
	payload = {"datapoints":[{"dataChnId":dataChnId8,"values":{"value":1}}, {"dataChnId":dataChnId9,"values":{"value":1}}]}
	post_to_mcs(payload)

def checkWeatherState(temperature, humidity, dust):

	myApp.frames["StartPage"].temperatureData["text"] = temperature + " 度"
	myApp.frames["StartPage"].humidityData["text"] = humidity + " %"
	myApp.frames["StartPage"].dustData["text"] = dust

	if int(temperature) > 30:
		myApp.frames["StartPage"].temperatureData["fg"] = "red"
	elif int(temperature) < 10:
		myApp.frames["StartPage"].temperatureData["fg"] = "blue"
	else:
		myApp.frames["StartPage"].temperatureData["fg"] = "green"

	if int(humidity) > 90:
		myApp.frames["StartPage"].humidityData["fg"] = "red"
	elif int(humidity) < 30:
		myApp.frames["StartPage"].humidityData["fg"] = "blue"
	else:
		myApp.frames["StartPage"].humidityData["fg"] = "green"

	if int(dust) < 50:
		myApp.frames["StartPage"].dustData["fg"] = "green"
	elif int(dust) > 400:
		myApp.frames["StartPage"].dustData["fg"] = "red"
	elif int(dust) < 400 and int(dust) > 250:
		myApp.frames["StartPage"].dustData["fg"] = "orange"
	else:
		myApp.frames["StartPage"].dustData["fg"] = "yellow"


class RaspberryDisplay(Frame):

	def __init__(self, master=None):
		Frame.__init__(self,master)
		# self.pack(side="top", fill="both", expand=True)
		# self.grid_rowconfigure(0, weight=1)
		# self.grid_columnconfigure(0, weight=1)
		self.grid()

		self.frames = {}
		for F in (StartPage, MessagePage, SchedulePage):
			page_name = F.__name__
			frame = F(parent=root, controller=self)
			self.frames[page_name] = frame
			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the on that is visible.
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("StartPage")

	def show_frame(self, page_name):
		# Show a frame for the given page name
		frame = self.frames[page_name]
		frame.tkraise()

class StartPage(Frame):

	def __init__(self, parent, controller):

		Frame.__init__(self, parent)
		self.controller = controller
		self.grid()
		self.creatWidgets()
		mqtt_client.loop_start()
		self.update_clock()
		self.update_information()
		# lambda: self.controller.update_clock("StartPage")

	def creatWidgets(self):

		self.timeMessage = Label(self)
		self.timeMessage["text"] = " "
		self.timeMessage["font"] = ('times', 16, 'bold')
		self.timeMessage["fg"] = "black"
		self.timeMessage.grid(row=0, column=0, columnspan=4)

		self.emergencyButton = Button(self)
		self.emergencyButton["text"] = "緊急"
		self.emergencyButton["bg"] = "red"
		self.emergencyButton["relief"] = "flat"
		self.emergencyButton["command"] = sendEmergence
		self.emergencyButton.grid(row=0, column=4)
# -------------------------------------------------------------
		self.temperatureLabel = Label(self)
		self.temperatureLabel["text"] = "溫度:"
		self.temperatureLabel["font"] = ('times', 14)
		self.temperatureLabel.grid(row=1, column=0)

		self.temperatureData = Label(self)
		self.temperatureData["text"] = "Loading"
		self.temperatureData["font"] = ('times', 14)
		self.temperatureData.grid(row=1, column=1)
# -------------------------------------------------------------
		self.humidityLabel = Label(self)
		self.humidityLabel["text"] = "溼度:"
		self.humidityLabel["font"] = ('times', 14)
		self.humidityLabel.grid(row=2, column=0)

		self.humidityData = Label(self)
		self.humidityData["text"] = "Loading"
		self.humidityData["font"] = ('times', 14)
		self.humidityData.grid(row=2, column=1) 
# --------------------------------------------------------------
		self.dustLabel = Label(self)
		self.dustLabel["text"] = "粉塵:"
		self.dustLabel["font"] = ('times', 14)
		self.dustLabel.grid(row=3, column=0)

		self.dustData = Label(self)
		self.dustData["text"] = "Loading"
		self.dustData["font"] = ('times', 14)
		self.dustData.grid(row=3, column=1)
# ------------------------------------------------------------- 
		self.notify = Label(self)
		self.notify["text"] = "Have a good day"
		self.notify["font"] =  ('times', 14, 'bold')
		self.notify.grid(row=4, column=0, columnspan=4, sticky=E)
# -------------------------------------------------------------
		self.messageButton = Button(self)
		self.messageButton["text"] = "信息"
		self.messageButton["bg"] = "white"
		self.messageButton["fg"] = "blue"
		self.messageButton["command"] = lambda: self.controller.show_frame("MessagePage")
		self.messageButton.grid(row=5, column=0, sticky=W)

		self.scheduleButton = Button(self)
		self.scheduleButton["text"] = "課表"
		self.scheduleButton["bg"] = "white"
		self.scheduleButton["fg"] = "blue"
		self.scheduleButton["command"] = lambda: self.controller.show_frame("SchedulePage")
		self.scheduleButton.grid(row=5, column=4)

	def update_information(self):

		mqtt_client.on_connect = on_connect
		mqtt_client.on_message = on_message
		mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)
		# self.after(1000, self.update_information)
		

	def update_clock(self):

		now = time.strftime("%H:%M:%S")
		self.timeMessage.configure(text=now)
		self.after(100, self.update_clock)

class MessagePage(Frame):

	def __init__(self, parent, controller):

		Frame.__init__(self, parent)
		self.controller = controller
		self.grid()
		self.creatWidgets()

	def creatWidgets(self):

		self.timeMessage = Label(self)
		self.timeMessage["text"] = " "
		self.timeMessage["font"] = ('times', 16, 'bold')
		self.timeMessage.grid(row=0, column=0, columnspan=5)

		self.messageBox = Listbox(self)
		# self.messageBox["textvariable"] = messageText
		self.messageBox["font"] = ('times', 14, 'bold')
		self.messageBox["fg"] = "blue"
		self.messageBox["bg"] = "grey"
		self.messageBox["width"] = 18
		self.messageBox['height'] = 5
		self.messageBox.grid(row=1, column=0, rowspan=3, columnspan=5)

		self.backButton = Button(self)
		self.backButton["text"] = "返回"
		self.backButton["command"] = lambda: self.controller.show_frame("StartPage")
		self.backButton.grid(row=5, column=2)

class SchedulePage(Frame):
	def __init__(self, parent, controller):

		Frame.__init__(self, parent)
		self.controller = controller
		self.grid()
		self.creatWidgets()

	def creatWidgets(self):
		self.backButton = Button(self)
		self.backButton["text"] = "返回"
		self.backButton["command"] = lambda: self.controller.show_frame("StartPage")
		self.backButton.grid(row=1, column=0)



if __name__ == "__main__":
	root = Tk()
	mqtt_client = mqtt.Client()
	myApp = RaspberryDisplay(master=root)
	myApp.master.title("Intelegent Bag")
	myApp.mainloop()