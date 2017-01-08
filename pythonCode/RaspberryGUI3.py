
import paho.mqtt.client as mqtt
import time
from Tkinter import *
import Tkinter as tk
import datetime

#----------------------------------------------------------------------
r_height = 300     #window size
r_width = 395        
root = Tk()  
root.geometry(str(r_width) + "x" + str(r_height))         #set the window size
root.configure(background='black')                        #set the background to be black
#----------------------------------------------------------------------------------------------
message_button = tk.BooleanVar()
message_button.set(True)
p_message_button = tk.BooleanVar()  
task_button = tk.BooleanVar()
p_task_button = tk.BooleanVar()
emergency_button = 0      # 0: no danger  1: sending danger singnal  2: receive danger signal
record_button = tk.BooleanVar()
record_button.set(False)
p_record_button = tk.BooleanVar()
announcement_button = tk.BooleanVar()
p_announcement_button = tk.BooleanVar()
information_come = False      # used to record whether there is announcement coming
information_come_time = [datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()]   # used to record the time that information came

#fake
temperature_data = 11
humidity_data = 100
#------------------------------------------------------------------------------------------------
#information setup
mon = ['Mon', '\n', 'Chinese','Math','Math','English', '\n', 'noon', '\n', 'Society','Science','Exercise']
tue = ['Tue', '\n', 'Chinese','Math','Math','English', '\n', 'noon', '\n', 'Society','Science','Exercise']
wed = ['Wed', '\n', 'Chinese','Math','Math','English', '\n', 'noon', '\n', 'Society','Science','Exercise']
thu = ['Thu', '\n', 'Chinese','Math','Math','English', '\n', 'noon', '\n', 'Society','Science','Exercise']
fri = ['Fri', '\n', 'Chinese','Math','Math','English', '\n', 'noon', '\n', 'Society','Science','Exercise']
start_place_x = 10.0/395*r_width
start_place_y = 10.0/300*r_height
offset = 50
width_of_list = 8
millis_i = int(round(time.time()*1000))            #system initial time
def EM():
	global emergency_button
	if emergency_button == 0:
		emergency_button = 1
	elif emergency_button == 1:
		emergency_button = 0
	print "EM"		
def millis():
	millis = int(round(time.time()*1000))-millis_i
	return millis

record = ["Time Record", "\n", "Mon: 8:30", "Tue: 7:40"]

information = ["Go Home !", "ya", "yes"]
#---------------------------------------------------------------------------------------
#MQTT setup
deviceId = "DbXmvM7r"
deviceKey = "Nsu1XDpbtXst8JY2"
MQTT_SERVER = "mqtt.mcs.mediatek.com"
MQTT_PORT = 1883
MQTT_ALIVE = 60
#MQTT_TOPIC_ALL = "mcs/" + deviceId + "/" + deviceKey + "/+"
MQTT_TOPIC = "mcs/" + deviceId + "/" + deviceKey + "/+"
def on_connect(client, userdata, flags, rc):
    print("MQTT Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)
def on_message(client, userdata, msg):
	print("mqtt payload=%s" %(msg.payload))
	device_name = msg.payload.split(',')[1]
	data = msg.payload.split(',')[2]
	decision(data, device_name)
def decision(data, device_name):
	if (device_name == 'LED_control'):
		print data
		global emergency_button
		global information_come
		global information_come_time
		global information
		if (data == "0"):
			#emergency_button = 0
			information_come = False	
		if (data == "1"):
			#emergency_button = 2
			information_come = True
			information_come_time.insert(len(information), datetime.datetime.now())
			information.insert(len(information), "hi")
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)
def Danger_Message():
	background_color = 'black'
	if emergency_button == 1 :
		sug = "Danger! Emergence singal sending !"
	  	suggestion = Message(root, bg='black', foreground='red', text=sug,  width = int(300.0/395*r_width))
		suggestion.pack()                                                    
		suggestion.place(bordermode=OUTSIDE, x=30.0/395*r_width, y=150.0/300*r_height)

	elif emergency_button == 2 :
		dan = "Danger! Emergence singal reveived !"
	  	suggestion = Message(root, bg='black', foreground='red', text=dan,  width = int(300.0/395*r_width)) 
		suggestion.pack()                                                    
		suggestion.place(bordermode=OUTSIDE, x=30.0/395*r_width, y=150.0/300*r_height)
#-----------------------------------------------------------------------------------------
def Decorate():
	global background_color
	background_color = 'black'
	if emergency_button != 0 :
		if millis() % 200 > 100:
			background_color = 'red'
		else:
			background_color = 'black' 
	listb  = Listbox(height=23, width=int(float(width_of_list*4+2)/395*r_width), bg=background_color, bd=20)     #height and width to deside the size of listbox    		
	listb.pack()                              #pack listbox to show on the window           
	listb.place(bordermode=OUTSIDE, x=0, y=0)              #change the position of the listbox
#----------------------------------------------------------------------------------------
def show_message():
	Temperature = Message(root, bg='black', foreground='white', text="Temperature",  width = int(100.0/395*r_width)) 
	Temperature.pack()                                                    
	Temperature.place(bordermode=OUTSIDE, x=50.0/395*r_width, y=50.0/300*r_height)       
	Temperature_data = Message(root, bg='black', foreground='white', text=str(temperature_data)+" deg",  width = int(100.0/395*r_width))   
	Temperature_data.pack()                                                    
	Temperature_data.place(bordermode=OUTSIDE, x=150.0/395*r_width, y=50.0/300*r_height)   

	Humidity = Message(root, bg='black', foreground='white', text="Humidity",  width = int(100.0/395*r_width))  
	Humidity.pack()                                                    
	Humidity.place(bordermode=OUTSIDE, x=50.0/395*r_width, y=80.0/300*r_height)       
	Humidity_data = Message(root, bg='black', foreground='white', text=str(humidity_data)+" %",  width = int(100.0/395*r_width))  
	Humidity_data.pack()                                                    
	Humidity_data.place(bordermode=OUTSIDE, x=150.0/395*r_width, y=80.0/300*r_height)  

	PM25 = Message(root, bg='black', foreground='white', text="PM25",  width = int(100.0/395*r_width))   
	PM25.pack()                                                    
	PM25.place(bordermode=OUTSIDE, x=50.0/395*r_width, y=110.0/300*r_height)       
	PM25_data = Message(root, bg='black', foreground='white', text="0",  width = int(100.0/395*r_width))   
	PM25_data.pack()                                                    
	PM25_data.place(bordermode=OUTSIDE, x=150.0/395*r_width, y=110.0/300*r_height)  

	sug = ""
	if temperature_data < 25:
		sug = "It's a little cool now, it's better to have a coat !"
	if temperature_data < 15:
		sug = "It's cold now, it's better to have a sweater !"
	if humidity_data > 40:
		sug = sug + "\n" + "\n" + "It's like to rain today, remember to bring an umbrella !"
	suggestion = Message(root, bg='black', foreground='green', text=sug,  width = int(200.0/395*r_width)) 
  	suggestion.place(bordermode=OUTSIDE, x=30.0/395*r_width, y=150.0/300*r_height)          
#---------------------------------------------------------------------------------------------------------------
def task():
	monlist  = Listbox(height=r_height, width=width_of_list, bg=background_color, fg='white')
	for item in mon:                           #put the data inside the listbox
	    monlist.insert(20,item)
	monlist.pack()                              #pack listbox to show on the window
	monlist.place(bordermode=OUTSIDE, x=start_place_x, y=start_place_y)              #change the position of the listbox
	#------------------------------------------------------------------------------------------------
	tuelist  = Listbox(height=r_height, width=width_of_list, bg=background_color, fg='white')
	for item in tue:                           #put the data inside the listbox
	    tuelist.insert(20,item)
	tuelist.pack()                              #pack listbox to show on the window
	tuelist.place(bordermode=OUTSIDE, x=start_place_x+offset, y=start_place_y)              #change the position of the listbox
	#------------------------------------------------------------------------------------------------
	wedlist  = Listbox(height=r_height, width=width_of_list, bg=background_color, fg='white')
	for item in wed:                           #put the data inside the listbox
	    wedlist.insert(20,item)
	wedlist.pack()                              #pack listbox to show on the window
	wedlist.place(bordermode=OUTSIDE, x=start_place_x+2*offset, y=start_place_y)              #change the position of the listbox
	#------------------------------------------------------------------------------------------------
	thulist  = Listbox(height=r_height, width=width_of_list, bg=background_color, fg='white')
	for item in thu:                           #put the data inside the listbox
	    thulist.insert(20,item)
	thulist.pack()                              #pack listbox to show on the window
	thulist.place(bordermode=OUTSIDE, x=start_place_x+3*offset, y=start_place_y)              #change the position of the listbox
	#------------------------------------------------------------------------------------------------
	frilist  = Listbox(height=r_height, width=width_of_list, bg=background_color, fg='white')
	for item in fri:                           #put the data inside the listbox
	    frilist.insert(20,item)
	frilist.pack()                              #pack listbox to show on the window
	frilist.place(bordermode=OUTSIDE, x=start_place_x+4*offset, y=start_place_y)              #change the position of the listbox
#------------------------------------------------------------------------------------------------------------------------------
def Emergence_Switch():
	emergency = Button(root, text="Emergency Button", command=EM, activebackground='green', bg='red', fg='white', height=3, relief=RIDGE, width=int(15.0/395*r_width))
	#emergency = Menubutton ( root, text="MENU", relief=RAISED, activebackground='red', cursor="hand2", width=20)
	emergency.pack()
	emergency.place(bordermode=OUTSIDE, x=280.0/395*r_width, y=250.0/300*r_height)
#------------------------------------------------------------------------------------------------------------------
def Menu_Button():
	menu_name = ""
	if message_button.get() == True:
		menu_name = "Main"
	elif task_button.get() == True:
		menu_name = "Schedule"
	elif record_button.get() == True:
		menu_name = "Time Record"
	elif announcement_button.get() == True:
		menu_name = "Announcement"
	mb = Menubutton ( root, text=menu_name, relief=RAISED, activebackground='green', cursor="hand2", width=int(15.0/395*r_width))
	mb.grid()
	mb.menu = Menu (mb, tearoff = 0)
	mb["menu"] = mb.menu 
	p_message_button.set(message_button.get())
	mb.menu.add_checkbutton ( label="Main", onvalue=True, offvalue=False, variable=message_button)
	p_task_button.set(task_button.get())
	mb.menu.add_checkbutton ( label="Schedule", onvalue=True, offvalue=False, variable=task_button )
	p_record_button.set(record_button.get())
	mb.menu.add_checkbutton ( label="Time Record", onvalue=True, offvalue=False, variable=record_button)
	p_announcement_button.set(announcement_button.get())
	if announcement_button.get():
		mb.menu.add_checkbutton ( label="Clean(" +str(len(information)) + ")", onvalue=True, offvalue=False, variable=announcement_button)
	else:
		mb.menu.add_checkbutton ( label="Announcement("+str(len(information)) + ")", onvalue=True, offvalue=False, variable=announcement_button)
	mb.pack()
	mb.place(bordermode=OUTSIDE, x=280.0/395*r_width, y=0)
#---------------------------------------------------------------------------------------------------------
def Record_Award():
	recordlist  = Listbox(height=r_height, width=width_of_list*4+4, bg=background_color, fg='white')
	for item in record:                           #put the data inside the listbox
	    recordlist.insert(20,item)
	recordlist.pack()                              #pack listbox to show on the window
	recordlist.place(bordermode=OUTSIDE, x=start_place_x, y=start_place_y)              #change the position of the listbox
#----------------------------------------------------------------------------------------------------------
def Screen_Refresh(color_in):
	screen  = Listbox(height=r_height, width=r_width, bg=color_in)     #height and width to deside the size of listbox     
	screen.pack()                              #pack listbox to show on the window           
	screen.place(bordermode=OUTSIDE, x=0, y=0)              #change the position of the listbox
	Emergence_Switch()
#----------------------------------------------------------------------------------------------------------
def Announcement():
	global information
	
	i = 0
	for item in information:
		announce = Message(root, bg='black', foreground='white', text=item + "  --- " + information_come_time[i].strftime("%Y/%m/%d %H:%M:%S"), width = 1000) 
		announce.pack()                                                    
		announce.place(bordermode=OUTSIDE, x=20.0/395*r_width, y=float(50+i*30)/300*r_height)
		i = i+1    	
#------------------------------------------------------------------------------------------------------------
def Information_come():
	notice = Message(root, bg='green', foreground='black', text=str(information_come_time[len(information_come_time)-1].strftime("%Y-%m-%d %H:%M:%S")) + "\n" + "Announcement :" + "\n" + information[len(information)-1],  width = 200.0/395*r_width, justify=CENTER) 
	notice.pack()                                                    
	#notice.place(bordermode=OUTSIDE, x=289, y=150) 
	notice.place(bordermode=OUTSIDE, x=float(r_width/2-70)/395*r_width, y=r_height/2)
#------------------------------------------------------------------------------------------------------------
def main_process():
	if(p_announcement_button.get() == True and announcement_button.get() == False):
		global information
		information = []
		information_come_time = []

	if (message_button.get() != p_message_button.get()) and (message_button.get() == True):
		Screen_Refresh('black')
		task_button.set(False)
		#p_task_button.set(False)
		record_button.set(False)
		#p_record_button.set(False)
		announcement_button.set(False)
		#p_announcement_button.set(False)
	elif (task_button.get() != p_task_button.get()) and (task_button.get() == True):
		Screen_Refresh('black')
		message_button.set(False)
		#p_message_button.set(False)
		record_button.set(False)
		#p_record_button.set(False)
		announcement_button.set(False)
		#p_announcement_button.set(False)
	elif (record_button.get() != p_record_button.get()) and (record_button.get() == True):
		Screen_Refresh('black')
		message_button.set(False)
		#p_message_button.set(False)
		task_button.set(False)
		#p_task_button.set(False)
		announcement_button.set(False)
		#p_announcement_button.set(False)
	elif (announcement_button.get() != p_announcement_button.get()) and (announcement_button.get() == True):
		Screen_Refresh('black')
		message_button.set(False)
		#p_message_button.set(False)
		task_button.set(False)
		#p_task_button.set(False)
		record_button.set(False)
		#p_record_button.set(False)
	elif announcement_button.get()==False and record_button.get()==False and task_button.get()==False and message_button.get()==False:
		Screen_Refresh('black')
		message_button.set(True)
	Decorate()
	if message_button.get() == True:
		show_message()
	elif task_button.get() == True:
		task()
	elif record_button.get() == True:
		Record_Award()
	elif announcement_button.get() == True:
		information_come = False
		Announcement()
	#----------------------------------------------------------------------------------------------
	Menu_Button()
	Danger_Message()
	global information_come
	if information_come:
		Information_come()
	




main_process()
Emergence_Switch()        #set the emergency button
while True:
	root.update()
	mqtt_client.loop_start()
	main_process()
	temperature_data = temperature_data + 0.1
	humidity_data = humidity_data - 1
	
	time.sleep(0.1)

	
	
