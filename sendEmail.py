#!/usr/bin/python
#-*- coding: utf-8 -*-
import smtplib
import sys, os
import getpass
import commands

from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import Encoders

naver_id = raw_input("Input Naver ID : ")
password = getpass.getpass()
from_addr = naver_id + "@naver.com"
smtp_id = naver_id

s = smtplib.SMTP_SSL('smtp.naver.com',465)
s.login(smtp_id, password)
s.quit()

subject = raw_input("Input Email Subject : ")
to_addr = raw_input("Input email address to receive mail : ")
print "----------- Input Text ------------ (Stop -> ^D)"
text = ""
while True:
	try:
		line = raw_input()
	except:
		break
	text += "%s\n" % line

msg=MIMEMultipart()

msg['Subject'] = subject
msg['From'] = from_addr
msg['To'] = to_addr
msg.attach(MIMEText(text, 'plain', 'utf-8'))

check = raw_input("Do you have attachment?? input(Y/N)>> ")
if check=="Y" or check=="y":
	attach_exists = True
else:
	attach_exists = False

if attach_exists:
	print "-------- File Attach --------- (Stop -> ^D)"
	file_name_list = []
	file_num = 0
	while True:
		try:
			file_name = raw_input("Input File Name #%d : " % (file_num+1))
		except:
			break
		file_name_list.append(file_name)
		part=MIMEBase('application','octet-stream')
		part.set_payload(open(os.path.abspath(file_name), 'rb').read())
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition','attachment; filename="%s"' % os.path.basename(file_name))
		msg.attach(part)
		file_num+=1

print 
print "-----------Review----------"
print "Subject : " + subject
print "From : " + from_addr
print "To : " + to_addr
print "----- Text -----"
print text

if attach_exists:
	for i in range(file_num):
		print "File #%d : %s" % (i+1,file_name_list[i])

print "---------------------------"
print
sel = raw_input("위 정보가 정확합니까? 입력(Y/N)>> ")
if not (sel=='Y' or sel=='y'):
    sys.exit()

s = smtplib.SMTP_SSL('smtp.naver.com',465)
s.login(smtp_id, password)
s.sendmail(from_addr, to_addr, msg.as_string())
s.quit()

print
print "Send mail Okay!"
print 
print "All progress was finished!!"
print
print "             Thank you :)"
print
