#coding:gbk

import sys,os
import re
import predict_sam_1
import urllib
#print sys.getdefaultencoding()

from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import shutil  
from urllib import unquote
import tensorflow as tf
from six.moves import cPickle
from utils_sam import TextLoader
from model_sam_2 import Model
from six import text_type


## SAM
save_dir = "save"
n = 100
sample = 1
global chars
global vocab
with open(os.path.join(save_dir, 'config.pkl'), 'rb') as f:
    saved_args = cPickle.load(f)
with open(os.path.join(save_dir, 'chars_vocab.pkl'), 'rb') as f:
    chars, vocab = cPickle.load(f)

model = Model(saved_args, True)
ret = ""
global sess
with  tf.Session() as sess:
    tf.initialize_all_variables().run()
    saver = tf.train.Saver(tf.all_variables())
    ckpt = tf.train.get_checkpoint_state(save_dir)
    print("--ckpt infos ----------------")
    print(ckpt)
    print(ckpt.model_checkpoint_path)
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt.model_checkpoint_path)
    else:
        print("ERROR: Fail to load model....")
#sys.stdout.write("[�������]:%s" % ret.encode("gbk"))
#return ret.encode("gbk")

i = 1
class MyHttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):                     #��ӦGET����)
        print self.path.decode("utf-8")                  #��ӡ�ͻ�������GET��·��
        enc="UTF-8"

        query = self.path.decode("utf-8").encode("gbk")
        #query = urllib.unquote_plus(self.path.lstrip('/query=')).decode('utf8').encode('gb18030')
        print "pa query:" + query
        #result = predict_sam_1.sample(query,sess);
        result = model.sample(sess, chars, vocab, n, query, sample)
        result = result.encode("gbk")
        print "result = ",result
        #result = 'acb'
        #print "pa result:" + result.decode("gbk")

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
httpd.serve_forever()  #����http������2017/8/25 15:30:26)))))))))

