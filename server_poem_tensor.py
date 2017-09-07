#coding:gbk

import sys
import re
import predict_sam_1
import urllib
#print sys.getdefaultencoding()

from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import shutil  
from urllib import unquote

class MyHttpHandler(BaseHTTPRequestHandler):
	def do_GET(self):                     #响应GET请求)
		print self.path.decode("utf-8")                  #打印客户端请求GET的路径
		enc="UTF-8"

		query = self.path.decode("utf-8").encode("gbk")
		#query = urllib.unquote_plus(self.path.lstrip('/query=')).decode('utf8').encode('gb18030')
		print "tensor pa query:" + query
		result = predict_sam_1.sample(query);
		#result = ''
		print "tensor pa result:" + result.decode("gbk")

		self.send_response(200)           #发送200状态码，表示处理正常)
		self.send_header("Content-type", "text/html; charset=%s" % enc)   
		#发送html头，这里可说明文件类型和字符集等信息)
		self.send_header("Content-Length", str(len(result)))    
		#发送html头说明文件长度 注意，这里如果长度和实际长度不一致的话，
		#后面客户端处理时就会触发IncompleteRead 这个异常。
		self.end_headers()                #html头部分结束
		self.wfile.write(result)            #以刚才读出的那个文件的内容作为后续内容发出给http客户端

httpd=HTTPServer(("", 9999), MyHttpHandler) 
httpd.serve_forever()  #启动http服务器2017/8/25 15:30:26)))))))))
