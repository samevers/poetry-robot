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
	def do_GET(self):                     #响应GET请求)
		
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
		self.send_response(200)           #发送200状态码，表示处理正常)
		self.send_header("Content-type", "text/html; charset=%s" % enc)   
		#发送html头，这里可说明文件类型和字符集等信息)
		self.send_header("Content-Length", str(len(result)))    
		#发送html头说明文件长度 注意，这里如果长度和实际长度不一致的话，
		#后面客户端处理时就会触发IncompleteRead 这个异常。
		self.end_headers()                #html头部分结束
		self.wfile.write(result)            #以刚才读出的那个文件的内容作为后续内容发出给http客户端


httpd=HTTPServer(("", 6969), MyHttpHandler) 
print("Server started port 6969….")
httpd.serve_forever()  


#启动http服务器2017/8/25 15:30:26)))))))))
#def getResult(query) :
#
#	conn = httplib.HTTPConnection("127.0.0.1:9999")
#	data1 = '';
#	print "main subFun: query" + query
#	try:
#		conn.request("GET", query)
#		r1 = conn.getresponse()
#		print r1.status, r1.reason         #打印响应码和响应状态信息
#		data1 = r1.read()         #读响应内容
#	except:
#		print "exception!"
#	finally:
#		print "read response!"
#	print "main subFun: result:" + data1               #打印响应内容
#	conn.close()
#	return data1


