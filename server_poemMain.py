#coding:gbk

import sys
import re
import predict_sam_1
import urllib
import httplib
#print sys.getdefaultencoding()

import chardet
from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import shutil  
from urllib import unquote
import os

class MyHttpHandler(BaseHTTPRequestHandler):
	def do_GET(self):                     #��ӦGET����)
		
		query = self.path
		qencoding = chardet.detect(query)
		qenc = qencoding['encoding']

		print "query encoding:" + qencoding['encoding']

		if qenc.find("utf") != -1 :
			query = query.decode("utf-8").encode("gbk")
	
		print "query:" + query

		os.system('python /search/odin/yonghuahu/tmp/poetry-robot/test.py ' + query)
		#query = urllib.unquote_plus(self.path.lstrip('/query=')).decode('utf8').encode('gb18030')
		#result = getResult(query)
		file = open('poem.out', 'r')
		result = '';
		for it in file.readlines() :
			it = it.strip()
			result = it

		print "pa query:" + query
		print "pa result:" + result

		enc="UTF-8"
		self.send_response(200)           #����200״̬�룬��ʾ��������)
		self.send_header("Content-type", "text/html; charset=%s" % enc)   
		#����htmlͷ�������˵���ļ����ͺ��ַ�������Ϣ)
		self.send_header("Content-Length", str(len(result)))    
		#����htmlͷ˵���ļ����� ע�⣬����������Ⱥ�ʵ�ʳ��Ȳ�һ�µĻ���
		#����ͻ��˴���ʱ�ͻᴥ��IncompleteRead ����쳣��
		self.end_headers()                #htmlͷ���ֽ���
		self.wfile.write(result)            #�ԸղŶ������Ǹ��ļ���������Ϊ�������ݷ�����http�ͻ���


httpd=HTTPServer(("", 6969), MyHttpHandler) 
print("Server started port 6969��.")
httpd.serve_forever()  


#����http������2017/8/25 15:30:26)))))))))
#def getResult(query) :
#
#	conn = httplib.HTTPConnection("127.0.0.1:9999")
#	data1 = '';
#	print "main subFun: query" + query
#	try:
#		conn.request("GET", query)
#		r1 = conn.getresponse()
#		print r1.status, r1.reason         #��ӡ��Ӧ�����Ӧ״̬��Ϣ
#		data1 = r1.read()         #����Ӧ����
#	except:
#		print "exception!"
#	finally:
#		print "read response!"
#	print "main subFun: result:" + data1               #��ӡ��Ӧ����
#	conn.close()
#	return data1


