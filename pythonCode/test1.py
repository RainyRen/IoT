-*- coding:utf-8 -*-  

import os
import time
import ntplib
c = ntplib.NTPClient()
response = c.request('pool.ntp.org')
ts = response.tx_time
print ts
_date = time.strftime('%Y-%m-%d',time.localtime(ts))
_time = time.strftime('%X',time.localtime(ts))
print _time
os.system('date {} && time {}'.format(_date,_time)) 
print "----------------"
print (time.strftime("%d/%m/%Y"))
print (time.strftime("%H:%M:%S"))

  
# import socket  
# import struct  
# import time  
# # import win32api  
  
# TimeServer = '210.72.145.44' #国家授时中心ip  
# Port = 123  
  
# def getTime():  
#     TIME_1970 = 2208988800L  
#     client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
#     data = '\x1b' + 47 * '\0'  
#     client.sendto(data, (TimeServer, Port))  
#     data, address = client.recvfrom(1024)  
#     data_result = struct.unpack('!12I', data)[10]  
#     data_result -= TIME_1970  
#     return data_result  
  
# def setSystemTime():  
#     tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.gmtime(getTime())  
#     win32api.SetSystemTime(tm_year, tm_mon, tm_wday, tm_mday, tm_hour, tm_min, tm_sec, 0)  
#     print "Set System OK!"  
  
  
# # setSystemTime()  
# print "%d-%d-%d %d:%d:%d" % time.localtime(getTime())[:6]