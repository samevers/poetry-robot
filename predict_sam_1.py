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
from model_sam_2 import Model

from six import text_type


def sample(prime):
    save_dir = "save.3"
    n = 100
    sample = 1
    with open(os.path.join(save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(save_dir, 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = cPickle.load(f)
    print("--------------1") 
    model = Model(saved_args, True)
    print("--------------2") 
    ret = ""
    with tf.Session() as sess:
        print("--------------3") 
        print("--------------4") 
        tf.initialize_all_variables().run()
        print("--------------5") 
        saver = tf.train.Saver(tf.all_variables())
        print("--------------6") 
        ckpt = tf.train.get_checkpoint_state(save_dir)
        print("--------------7") 
        print("--ckpt infos ----------------")
        print(ckpt)
        print(ckpt.model_checkpoint_path)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            ret = model.sample(sess, chars, vocab, n, prime, sample)
        else:
            print("ERROR: Fail to load model....")
    sess.close()
    sys.stdout.write("[我是李白]:%s" % ret.encode("gbk"))
    return ret.encode("gbk")

