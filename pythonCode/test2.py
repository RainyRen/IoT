# Coding -*- utf-8 -*-
import httplib
import time
import os
def get_webservertime(host):
	conn=httplib.HTTPConnection(host)
	conn.request("GET", "/")
	r=conn.getresponse()
	ts= r.getheader('date')
	ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
	print(ltime)
	ttime=time.localtime(time.mktime(ltime)+8*60*60)
	print(ttime)
	dat="date %u-%02u-%02u"%(ttime.tm_year,ttime.tm_mon,ttime.tm_mday)
	tm="time %02u:%02u:%02u"%(ttime.tm_hour,ttime.tm_min,ttime.tm_sec)
	print (dat,tm)
	os.system(dat)
	os.system(tm)
     
get_webservertime('www.baidu.com')
print "--------------------------------"
print (time.strftime("%d/%m/%Y"))
print (time.strftime("%H:%M:%S"))