#-*- coding:utf-8 -*-
import serial
import time
import requests
import json
from email_mod import EmailSend

# -------------------------------------------------------
tStart = int(round(time.time()))

# Serial port initial
reading_time = 10
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM10'
ser.timeout = 1

# student list initial
attendance={}		# Record  every attendance situation
attendance_tmp=[]
# attendance = {"2016-12-30":[]}
absent_list=[]		# Record who is absent today
# -------------------------------------------------------
# stduent data
students = {4185164167:{'name':'Tom', 'phone': 917406000, 'email':'111@gmail.com'},
			2435592197:{'name':'Jerry', 'phone': 936888000, 'email':'222@gmail.com'},
			2328167202:{'name':'Tommy', 'phone': 932234761, 'email':'yulezhuanyongde@126.com'}
			}
# ------------------------------------------------------
# 云端数据库地址
firebase_url = 'https://rfiddata-dfbfc.firebaseio.com'

# -------------------------------------------------------
# 计算程式运行的时间
def processTime(starTime):
    rTime = int(round(time.time())) - starTime
    return rTime

# 将读取到的字符转换为数字
def read2num(s):
    try:
        return int(s)
    except ValueError:
        return 0

# 将迟到学生家长的邮件加入到发件列表中
def add_absent_list(a_list):
	absent_file = open("studnet_absent_list.txt", "w")
	
	for student in a_list:
		email_server.add_receivers(students[student]['email'])
		absent_file.write(students[student]['name']+'\n')

	absent_file.close()

# -------------------------------------------------------
try:
	date_today = time.strftime('%Y-%m-%d')

	attend_file = open("studnet_attendace_list.txt", "w")
	attend_file.write(date_today + '\n')

	attendance[date_today] = []
	ser.open()

	while processTime(tStart) < reading_time:
		tmp = ser.readline()

		if tmp != '':
			print tmp			
			tmp = read2num(tmp)
			enter_time = time.strftime('%H:%M:%S')
			attendance_tmp.append(tmp)
			attendance[date_today].append((tmp, enter_time))
			attend_file.write(str(tmp) + '@' + enter_time + '\n')
		
except KeyboardInterrupt:
	ser.close()
	attend_file.close()

print attendance
# attend_file.write(json.dumps(attendance))

for student in students:
	# print type(student)
	if student not in attendance_tmp:
		absent_list.append(student)
		print students[student]['name'] + "is late"

print absent_list

email_server = EmailSend()
add_absent_list(absent_list)
email_server.send_email()


ser.close()
attend_file.close()

# upload attendace data to cloud database
result = requests.post(firebase_url + '/attendanceList' + '.json', data=json.dumps(attendance))
# print result
print 'Status Code = ' + str(result.status_code) + ', Response = ' + result.text