
import paho.mqtt.client as mqtt
import time
from Tkinter import *
import Tkinter as tk

#----------------------------------------------------------------------
#MQTT setup
deviceId = "DbXmvM7r"
deviceKey = "Nsu1XDpbtXst8JY2"
MQTT_SERVER = "mqtt.mcs.mediatek.com"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_TOPIC_ALL = "mcs/" + deviceId + "/" + deviceKey + "/+"
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
emergency_button = tk.BooleanVar()
emergency_button.set(False)
record_button = tk.BooleanVar()
record_button.set(False)
p_record_button = tk.BooleanVar()

#fake
temperature_data = 11
humidity_data = 100
#----------------------------------------------------------------------------------------------



#-----------------------------------------------------------------
#information setup
mon = ['Mon', '\n', 'Chinese','Math','Math','English', '\n', 'noon', '\n', 'Society','Science','Exercise']
tue = ['Tue', '\n', 'Chinese','Math','Math','English', '\n', 'noon', '\n', 'Society','Science','Exercise']
wed = ['Wed', '\n', 'Chinese','Math','Math','English', '\n', 'noon', '\n', 'Society','Science','Exercise']
thu = ['Thu', '\n', 'Chinese','Math','Math','English', '\n', 'noon', '\n', 'Society','Science','Exercise']
fri = ['Fri', '\n', 'Chinese','Math','Math','English', '\n', 'noon', '\n', 'Society','Science','Exercise']
start_place_x = 10
start_place_y = 10
offset = 50
width_of_list = 8
millis_i = int(round(time.time()*1000))             #system initial time

def EM():
	if emergency_button.get() == False:
		emergency_button.set(True)
	else:
		emergency_button.set(False)
	print "EM"

def millis():
	millis = int(round(time.time()*1000))-millis_i
	return millis

record = ["Time Record", "\n", "Mon: 8:30", "Tue: 7:40"]
#---------------------------------------------------------------------------------------
def Decorate():
	if emergency_button.get() == True :
		if millis() % 200 > 100:
			Screen_Refresh('red')
			#listb  = Listbox(height=r_height, width=width_of_list*4+10, bg='red', bd=20)			
		else:
			Screen_Refresh('black')
			#listb  = Listbox(height=r_height, width=width_of_list*4+10, bg='black', bd=20)			
	else:
		listb  = Listbox(height=23, width=width_of_list*4+2, bg='black', bd=20)     #height and width to deside the size of listbox     		
		listb.pack()                              #pack listbox to show on the window           
		listb.place(bordermode=OUTSIDE, x=0, y=0)              #change the position of the listbox
#----------------------------------------------------------------------------------------
def show_message():
	Temperature = Message(root, bg='black', foreground='white', text="Temperature",  width = 100) 
	Temperature.pack()                                                    
	Temperature.place(bordermode=OUTSIDE, x=50, y=50)       
	Temperature_data = Message(root, bg='black', foreground='white', text=str(temperature_data)+" deg",  width = 100)   
	Temperature_data.pack()                                                    
	Temperature_data.place(bordermode=OUTSIDE, x=150, y=50)   

	Humidity = Message(root, bg='black', foreground='white', text="Humidity",  width = 100)  
	Humidity.pack()                                                    
	Humidity.place(bordermode=OUTSIDE, x=50, y=80)       
	Humidity_data = Message(root, bg='black', foreground='white', text=str(humidity_data)+" %",  width = 100)  
	Humidity_data.pack()                                                    
	Humidity_data.place(bordermode=OUTSIDE, x=150, y=80)  

	PM25 = Message(root, bg='black', foreground='white', text="PM25",  width = 100)   
	PM25.pack()                                                    
	PM25.place(bordermode=OUTSIDE, x=50, y=110)       
	PM25_data = Message(root, bg='black', foreground='white', text="0",  width = 100)   
	PM25_data.pack()                                                    
	PM25_data.place(bordermode=OUTSIDE, x=150, y=110)  

	# sug = ""
	if temperature_data < 25:
		sug = "It's a little cool now, it's better to have a coat !"
	if temperature_data < 15:
		sug = "It's cold now, it's better to have a sweater !"
	if humidity_data > 40:
		sug = sug + "\n" + "\n" + "It's like to rain today, remember to bring an umbrella !"
	suggestion = Message(root, bg='black', foreground='green', text=sug,  width = 200) 

	if emergency_button.get() == True:
		sug = "Danger! Emergence singal sending !"
	  	suggestion = Message(root, bg='black', foreground='red', text=sug,  width = 200)

	suggestion.pack()                                                    
	suggestion.place(bordermode=OUTSIDE, x=30, y=150)       	          
#---------------------------------------------------------------------------------------------------------------
def task():
	monlist  = Listbox(height=r_height, width=width_of_list, bg='black', fg='white')
	for item in mon:                           #put the data inside the listbox
	    monlist.insert(20,item)
	monlist.pack()                              #pack listbox to show on the window
	monlist.place(bordermode=OUTSIDE, x=start_place_x, y=start_place_y)              #change the position of the listbox
	#------------------------------------------------------------------------------------------------
	tuelist  = Listbox(height=r_height, width=width_of_list, bg='black', fg='white')
	for item in tue:                           #put the data inside the listbox
	    tuelist.insert(20,item)
	tuelist.pack()                              #pack listbox to show on the window
	tuelist.place(bordermode=OUTSIDE, x=start_place_x+offset, y=start_place_y)              #change the position of the listbox
	#------------------------------------------------------------------------------------------------
	wedlist  = Listbox(height=r_height, width=width_of_list, bg='black', fg='white')
	for item in wed:                           #put the data inside the listbox
	    wedlist.insert(20,item)
	wedlist.pack()                              #pack listbox to show on the window
	wedlist.place(bordermode=OUTSIDE, x=start_place_x+2*offset, y=start_place_y)              #change the position of the listbox
	#------------------------------------------------------------------------------------------------
	thulist  = Listbox(height=r_height, width=width_of_list, bg='black', fg='white')
	for item in thu:                           #put the data inside the listbox
	    thulist.insert(20,item)
	thulist.pack()                              #pack listbox to show on the window
	thulist.place(bordermode=OUTSIDE, x=start_place_x+3*offset, y=start_place_y)              #change the position of the listbox
	#------------------------------------------------------------------------------------------------
	frilist  = Listbox(height=r_height, width=width_of_list, bg='black', fg='white')
	for item in fri:                           #put the data inside the listbox
	    frilist.insert(20,item)
	frilist.pack()                              #pack listbox to show on the window
	frilist.place(bordermode=OUTSIDE, x=start_place_x+4*offset, y=start_place_y)              #change the position of the listbox
#------------------------------------------------------------------------------------------------------------------------------
def Emergence_Switch():
	emergency = Button(root, text="Emergency Button", command=EM, activebackground='green', bg='red', fg='white', height=3, relief=RIDGE, width=15)
	#emergency = Menubutton ( root, text="MENU", relief=RAISED, activebackground='red', cursor="hand2", width=20)
	emergency.pack()
	emergency.place(bordermode=OUTSIDE, x=280, y=250)
#------------------------------------------------------------------------------------------------------------------
def Menu_Button():
	menu_name = ""
	if message_button.get() == True:
		menu_name = "Main"
	elif task_button.get() == True:
		menu_name = "Schedule"
	elif record_button.get() == True:
		menu_name = "Time Record"
	mb = Menubutton ( root, text=menu_name, relief=RAISED, activebackground='green', cursor="hand2", width=15)
	mb.grid()
	mb.menu = Menu (mb, tearoff = 0)
	mb["menu"] = mb.menu 
	p_message_button.set(message_button.get())
	mb.menu.add_checkbutton ( label="Main", onvalue=True, offvalue=False, variable=message_button)
	p_task_button.set(task_button.get())
	mb.menu.add_checkbutton ( label="Schedule", onvalue=True, offvalue=False, variable=task_button )
	p_record_button.set(record_button.get())
	mb.menu.add_checkbutton ( label="Time Record", onvalue=True, offvalue=False, variable=record_button)
	mb.pack()
	mb.place(bordermode=OUTSIDE, x=280, y=0)
#---------------------------------------------------------------------------------------------------------
def Record_Award():
	recordlist  = Listbox(height=r_height, width=width_of_list*4+4, bg='black', fg='white')

	for item in record:                           #put the data inside the listbox
	    recordlist.insert(20,item)
	recordlist.pack()                              #pack listbox to show on the window

	recordlist.place(bordermode=OUTSIDE, x=start_place_x, y=start_place_y)              #change the position of the listbox
#----------------------------------------------------------------------------------------------------------
def Screen_Refresh(color_in):
	screen  = Listbox(height=r_height, width=r_width, bg=color_in)     #height and width to deside the size of listbox     
	screen.pack()                              #pack listbox to show on the window           
	screen.place(bordermode=OUTSIDE, x=0, y=0)              #change the position of the listbox
	Emergence_Switch()        #set the emergency button
#----------------------------------------------------------------------------------------------------------
def main_process():
	Decorate()
	if (message_button.get() != p_message_button.get()) and (message_button.get() == True):
		Screen_Refresh('black')
		task_button.set(False)
		p_task_button.set(False)
		record_button.set(False)
		p_record_button.set(False)
	elif (task_button.get() != p_task_button.get()) and (task_button.get() == True):
		Screen_Refresh('black')
		message_button.set(False)
		p_message_button.set(False)
		record_button.set(False)
		p_record_button.set(False)
	elif (record_button.get() != p_record_button.get()) and (record_button.get() == True):
		Screen_Refresh('black')
		message_button.set(False)
		p_message_button.set(False)
		task_button.set(False)
		p_task_button.set(False)
	if message_button.get() == True:
		show_message()
	elif task_button.get() == True:
		task()
	elif record_button.get() == True:
		Record_Award()
	#----------------------------------------------------------------------------------------------
	Menu_Button()
	




main_process()
Emergence_Switch()        #set the emergency button
while True:
	root.update()

	if(message_button.get() != p_message_button.get()):
		main_process()
		
	temperature_data = temperature_data + 0.1
	humidity_data = humidity_data - 1
	time.sleep(0.1)

	
	
