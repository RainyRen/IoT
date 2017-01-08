#-*- coding:utf-8 -*- 

import smtplib
import base64
from email.mime.text import MIMEText
from email.header import Header

class EmailSend():
	def add_receivers(self, user):
		self.receivers.append(user)

	def add_receivers_list(self, userList):
		self.receivers = self.receivers + userList

	def modify_email_host(self, user_id, user_pass):
		self.mail_user = user_id
		self.mail_pass = user_pass

	def add_subject(self, subjet):
		self.message['Subject'] = Header(subjet, 'utf-8')


	mail_host="smtp.gmail.com"  #设置服务器
	mail_user=""    #用户名
	mail_pass=base64.b64decode("")   #口令

	sender = mail_user
	receivers = []  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

	# 读取文档的内容作为信件内容
	fe = open("emailContent.txt", 'rb')
	message = MIMEText(fe.read())
	fe.close()

	message['From'] = Header("NTPS")
	# message['To'] =  Header(''.join(receivers))
	subject = 'Late Information (from NTPS)'
	message['Subject'] = Header(subject, 'utf-8')

	# 发送邮件到所有收件人
	def send_email(self):
		try:
			self.message['To'] = Header(''.join(self.receivers))
			smtpServer = smtplib.SMTP() 
			smtpServer.connect(self.mail_host, 587)    # 587 为 SMTP 端口号
			smtpServer.ehlo()
			smtpServer.starttls()
			smtpServer.login(self.mail_user,self.mail_pass)  
			smtpServer.sendmail(self.sender, self.receivers, self.message.as_string())
			smtpServer.close()
			print "Send successful"


		except smtplib.SMTPException:
		    print "Error: Send fail"
		    smtpServer.close()

# server = EmailSend()
# server.add_receivers('yulezhuanyongde@126.com;')
# server.send_email()
# print server.message
