#!/usr/bin/python
#coding:gbk
from __future__ import print_function
import numpy as np
import tensorflow as tf

import argparse
import time
import os,sys
from six.moves import cPickle

from utils_sam import TextLoader
from model_sam import Model

from six import text_type
import predict_sam_1
#import predict_test

sess = tf.Session() 
if __name__ == '__main__':
    #prime  = raw_input('> Begin with: ')
    #filename=  sys.argv[1]
    #fin = open(filename, 'r')
    #prime = fin.readline()
    #fin.close()
    prime = sys.argv[1]
    ret = predict_sam_1.sample(prime)
    outfile = "poem.out"
    fout = open(outfile, 'w')
    fout.write("%s" % ret)
    fout.close()
    #sys.stdout.write("%s\n" % ret)
