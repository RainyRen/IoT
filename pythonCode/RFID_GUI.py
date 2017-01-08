#-*- coding:utf-8 -*-  
# ------------------------------------------------------
# 腳位設定：
# 由上至下：10 13 11 12 空 GND A0 3.3V
# ------------------------------------------------------
from Tkinter import *
import time
import serial
import requests
import json
from email_mod import EmailSend


date_today = time.strftime('%Y-%m-%d')
reading_time = 20

# Serial port initial
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM10'
ser.timeout = 1

# student list initial
attendance={}       # Record  every attendance situation
attendance_tmp=[]
absent_list=[]      # Record who is absent today
# -------------------------------------------------------
# stduent data
students = {4185164167:{'name':'Tom', 'phone': 917406000, 'email':'111@gmail.com'},
            2435592197:{'name':'Jerry', 'phone': 936888000, 'email':'222@gmail.com'},
            2328167202:{'name':'Tommy', 'phone': 932234761, 'email':''},
            
            }
# ------------------------------------------------------
# 云端数据库地址
firebase_url = 'https://rfiddata-dfbfc.firebaseio.com'

# -------------------------------------------------------
class RFIDDisplay(Frame):
    restTime = 5
    student_rank = 0

    tStartTime = int(round(time.time()))


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def processTime(self, starTime):
        rTime = int(round(time.time())) - starTime
        return rTime

    def read2num(self, s):
        try:
            return int(s)
        except ValueError:
            return 0

    def add_absent_list(self, a_list):
        absent_file = open("studnet_absent_list.txt", "w")
        
        for student in a_list:
            email_server.add_receivers(students[student]['email'])
            absent_file.write(students[student]['name']+'\n')

        absent_file.close()

    def restDisplayText(self):

        if self.restCount == 0:
            self.displayText["text"] = "Good Morning"
            self.displayText["fg"] = "black"
            self.restCount = self.restTime
        else:
            self.restCount -= 1

    def startProgress(self):
        ser.close()
        self.restCount = self.restTime
        self.startTime()
        self.remindTime()

    def stopProgress(self):

        if self.remindTime_cancel_id is not None:
            self.after_cancel(self.remindTime_cancel_id)
            self.remindTime_cancel_id = None
            self.start.config(state="normal")
            self.stopButton.config(state="disabled")

    def startTime(self):
         self.tStartTime = int(round(time.time()))
         self.start.config(state="disabled")
         self.stopButton.config(state="normal")
         ser.open()

    def remindTime(self):        

        remind_time = reading_time - self.processTime(self.tStartTime)

        if remind_time < 0:
            print "Finshed"
            absent_namelist = []
            ser.close()
            attend_file.close()
            self.remindTimeText.configure(text="你遲到了哦！")
            self.stopProgress()

            for studentNumber in students:
                # print type(student)
                if studentNumber not in attendance_tmp:
                    absent_list.append(studentNumber)
                    absent_namelist.append(students[studentNumber]['name'])
                    print students[studentNumber]['name'] + "is late"

            self.add_absent_list(absent_list)
            result_attendance = requests.post(firebase_url + '/attendanceList' + '.json', data=json.dumps(attendance))
            result_absent = requests.post(firebase_url + '/absentList' + '.json', data=json.dumps(absent_namelist))
            # print email_server.message
            email_server.send_email()

            

        else:
            tmp = ser.readline()
            if tmp != '':
                print tmp          
                tmp = self.read2num(tmp)                #讀取的RFID字符轉換爲數字
                enter_time = time.strftime('%H:%M:%S')  #進入校園的時間
                if tmp in students.keys():
                    self.student_rank += 1                  #學生排位增加
                    self.infoField["text"] = students[tmp]['name'] 
                    self.placeField["text"] = enter_time + " 你的是第: " + str(self.student_rank) + "名"
                    self.displayText["text"] = "Permission"
                    self.displayText["fg"] = "green"
                    attendance_tmp.append(tmp)
                    attendance[date_today].append((students[tmp]['name'], enter_time))
                    attend_file.write(students[tmp]['name'] + ' @' + enter_time + '\n')
                    # self.restDisplayText()

                elif tmp != 0:
                    self.displayText["text"] = "Permisson Denied"
                    self.displayText["fg"] = "red"
                    # self.restDisplayText()
            else:
                self.restDisplayText()
                # pass
            # 更新時間
            self.remindTimeText.configure(text=remind_time)
            self.remindTime_cancel_id = self.after(10, self.remindTime)

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.timeMessage.configure(text=now)
        self.clock_cancel_id = self.after(10, self.update_clock)
 
    def createWidgets(self):

        self.start = Button(self)
        self.start["text"] = "START"
        self.start["fg"] = "blue"
        self.start["command"] = self.startProgress
        self.start.grid(row=0, column=0)
        self.timeMessage = Label(self)
        self.timeMessage["text"] = ""
        self.timeMessage["bg"] = "green" 
        self.timeMessage["font"] = ('times', 16, 'bold')
        self.timeMessage.grid(row=0, column=2, columnspan=4)

        self.infoLabel = Label(self)
        self.infoLabel["text"] = "Info:"
        self.infoLabel.grid(row=1, column=0, sticky=E)
        self.infoField = Label(self)
        self.infoField["font"] = ('times', 20, 'bold')
        self.infoField["width"] = 20
        self.infoField["height"] = 2
        self.infoField.grid(row=1, column=1, columnspan=6)
 
        self.placeText = Label(self)
        self.placeText["text"] = "Place:"
        self.placeText.grid(row=2, column=0, sticky=E)
        self.placeField = Label(self)
        self.placeField["font"] = ('times', 20)
        self.placeField["width"] = 20
        self.placeField["height"] = 2
        self.placeField.grid(row=2, column=1, columnspan=6)

        self.stopButton = Button(self)
        self.stopButton["text"] = "STOP"
        self.stopButton["fg"] = "blue" 
        self.stopButton.config(state="disabled")
        self.stopButton["command"] = self.stopProgress
        self.stopButton.grid(row=3, column=0)
        self.remindTimeText = Label(self)
        self.remindTimeText["text"] = ""
        self.remindTimeText["bg"] = "red"
        self.remindTimeText["font"] = ('times', 16, 'bold')
        self.remindTimeText.grid(row=3, column=2,columnspan=4)
        
        self.end = Button(self)
        self.end["text"] = "QUIT"
        self.end["fg"] = "red"
        self.end["command"] =  self.quit
        self.end.grid(row=4, column=0)
        self.displayText = Label(self)
        self.displayText["width"] = 20
        self.displayText["heigh"] = 2
        self.displayText["font"] = ('times', 16, 'bold')
        self.displayText["text"] = "Good Morning"
        self.displayText.grid(row=4, column=1, columnspan=7)
 
if __name__ == '__main__':   
    attend_file = open("studnet_attendace_list.txt", "w")
    attend_file.write(date_today + '\n')

    attendance[date_today] = []
    email_server = EmailSend()

    root = Tk()
    myApp = RFIDDisplay(master=root)
    myApp.master.title("School Sign In System")
    myApp.update_clock()
    # myApp.remindTime()
    myApp.mainloop()
