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
	def do_GET(self):                     #��ӦGET����)
		print self.path.decode("utf-8")                  #��ӡ�ͻ�������GET��·��
		enc="UTF-8"

		query = self.path.decode("utf-8").encode("gbk")
		#query = urllib.unquote_plus(self.path.lstrip('/query=')).decode('utf8').encode('gb18030')
		print "tensor pa query:" + query
		result = predict_sam_1.sample(query);
		#result = ''
		print "tensor pa result:" + result.decode("gbk")

		self.send_response(200)           #����200״̬�룬��ʾ��������)
		self.send_header("Content-type", "text/html; charset=%s" % enc)   
		#����htmlͷ�������˵���ļ����ͺ��ַ�������Ϣ)
		self.send_header("Content-Length", str(len(result)))    
		#����htmlͷ˵���ļ����� ע�⣬����������Ⱥ�ʵ�ʳ��Ȳ�һ�µĻ���
		#����ͻ��˴���ʱ�ͻᴥ��IncompleteRead ����쳣��
		self.end_headers()                #htmlͷ���ֽ���
		self.wfile.write(result)            #�ԸղŶ������Ǹ��ļ���������Ϊ�������ݷ�����http�ͻ���

httpd=HTTPServer(("", 9999), MyHttpHandler) 
httpd.serve_forever()  #����http������2017/8/25 15:30:26)))))))))
