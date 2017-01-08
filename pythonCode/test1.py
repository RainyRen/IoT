#-*- coding:utf-8 -*-  

import os
import time

# 系統校準方法
# import ntplib
# c = ntplib.NTPClient()
# response = c.request('pool.ntp.org')
# ts = response.tx_time
# print ts
# _date = time.strftime('%Y-%m-%d',time.localtime(ts))
# _time = time.strftime('%X',time.localtime(ts))
# print _time
# os.system('date {} && time {}'.format(_date,_time)) 
# print "----------------"
# print (time.strftime("%d/%m/%Y"))
# print (time.strftime("%H:%M:%S"))

# -------------------------------------------------------------------
# firease測試
# import json
# import requests
# from firebase import firebase
# firebase = firebase.FirebaseApplication('https://rfiddata-dfbfc.firebaseio.com', None)
# result = firebase.get('/2017-01-01', None)
# result = requests.get('https://rfiddata-dfbfc.firebaseio.com/studentList.json')
# students = json.loads(result.text)
# print students
# print result

#------------------------------------------------------------------------ 
# 時區校準
# TimeServer = '210.72.145.44' #国家授时中心ip  
# Port = 123  
  
# -------------------------------------------------------------------------------------
# 郵件測試
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header

# # 第三方 SMTP 服务
# mail_host="smtp.gmail.com"  #设置服务器
# mail_user=""    #用户名
# mail_pass=""   #口令 


# sender = ''
# receivers = ['']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# message = MIMEText('Python Email test')
# message['From'] = Header("NTPS")
# message['To'] =  Header("yulezhuanyongde@126.com")

# subject = 'Python SMTP 邮件测试'
# message['Subject'] = Header(subject, 'utf-8')

# try:
#     smtpServer = smtplib.SMTP() 
#     smtpServer.connect(mail_host, 587)    # 587 为 SMTP 端口号
#     smtpServer.ehlo()
#     smtpServer.starttls()
#     smtpServer.login(mail_user,mail_pass)  
#     smtpServer.sendmail(sender, receivers, message.as_string())
#     smtpServer.close()
#     print "Send successful"

# except smtplib.SMTPException:
#     print "Error: Send fail"

# from email_mod import EmailSend
# server = EmailSend()

# -----------------------------------------------------------------------------
# GUI顯示時鐘
# import sys    
# from Tkinter import *
# import time
# def tick():
#     global time1
#     # 从运行程序的计算机上面获取当前的系统时间
#     time2 = time.strftime('%H:%M:%S')
#     # 如果时间发生变化，代码自动更新显示的系统时间
#     if time2 != time1:
#         time1 = time2
#         clock.config(text=time2)
#         # calls itself every 200 milliseconds
#         # to update the time display as needed
#         # could use >200 ms, but display gets jerky
#     clock.after(200, tick)
# root = Tk()
# time1 = ''
# status = Label(root, text="v1.0", bd=1, relief=SUNKEN, anchor=W)
# status.grid(row=0, column=0)
# clock = Label(root, font=('times', 20, 'bold'), bg='green')
# clock.grid(row=0, column=1) 
# tick()
# root.mainloop()

# -------------------------------------------------------------------------------
# 密碼隱藏
# import base64
# print base64.b64encode("password")
# ------------------------------------------------------------------------------
# 網路獲取GPS信息
# import requests
# import json

# send_url = 'http://freegeoip.net/json'
# r = requests.get(send_url)
# j = json.loads(r.text)
# print j
# lat = j['latitude']
# lon = j['longitude']
# print lat
# print lon

awoke_time_H = 21
awoke_time_M = 44
awoke_time = "%02d : %02d" % (awoke_time_H, awoke_time_M)
print awoke_time