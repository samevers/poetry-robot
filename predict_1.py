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
from model_1 import Model

from six import text_type

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, default='save',
                       help='model directory to store checkpointed models')
    parser.add_argument('-n', type=int, default=500,
                       help='number of characters to sample')
    parser.add_argument('--prime', type=text_type, default=u'harasora',
                       help='prime text')
    parser.add_argument('--filename', type=text_type, default=u'test.txt',
                       help='prime file')
    parser.add_argument('--sample', type=int, default=1,
                       help='0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')

    args = parser.parse_args()
    sample(args)

def sample(args):
    with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = cPickle.load(f)
        #for ch in chars:
        #    print(ch.encode("gbk"))
        #for vo in vocab:
        #    print(vo.encode("gbk"))
		#exit()
    sys.stdout.write("length of chars: %d" % len(chars))

    model = Model(saved_args, True)
    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        saver = tf.train.Saver(tf.all_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        print("--ckpt infos ----------------")
        print(ckpt)
        print(ckpt.model_checkpoint_path)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            model.sample(sess, chars, vocab, args.filename, args.n, segId, args.prime, args.sample)

if __name__ == '__main__':
    main()
