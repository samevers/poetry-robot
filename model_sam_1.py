#!/usr/bin/python
#coding:gbk
import sys,os
#sys.path.append(".")
import tensorflow as tf
#sys.path.append("./tensorflow/python/ops")
#import rnn_cell
#import seq2seq
#from tensorflow.python.ops import rnn_cell
#from tensorflow.python.ops import seq2seq

from tensorflow.contrib.rnn.python.ops import core_rnn_cell
from tensorflow.contrib.legacy_seq2seq.python.ops import seq2seq
from tensorflow.python import nn

import numpy as np
class Model():
    def __init__(self, args, infer=False):
        self.args = args
        if infer:
            args.batch_size = 1
            args.seq_length = 1

        if args.model == 'rnn':
            cell_fn = core_rnn_cell.BasicRNNCell
        elif args.model == 'gru':
            cell_fn = core_rnn_cell.GRUCell
        elif args.model == 'lstm':
            cell_fn = core_rnn_cell.BasicLSTMCell
        else:
            raise Exception("model type not supported: {}".format(args.model))

        cell = cell_fn(args.rnn_size, state_is_tuple=True)

        self.cell = cell = core_rnn_cell.MultiRNNCell([cell] * args.num_layers, state_is_tuple=True) 

        self.input_data = tf.placeholder(tf.int32, [args.batch_size, args.seq_length], name="input_data")
        self.targets = tf.placeholder(tf.int32, [args.batch_size, args.seq_length], name="targets")
        self.initial_state = cell.zero_state(args.batch_size, tf.float32)

        with tf.variable_scope('rnnlm'):
            softmax_w = tf.get_variable("softmax_w", [args.rnn_size, args.vocab_size])
            softmax_b = tf.get_variable("softmax_b", [args.vocab_size])
            with tf.device("/cpu:0"):
                embedding = tf.get_variable("embedding", [args.vocab_size, args.rnn_size])
                print "seq_length = ", args.seq_length, "embedding_lookup = ", tf.nn.embedding_lookup(embedding, self.input_data)
                #inputs = tf.split(1, args.seq_length, tf.nn.embedding_lookup(embedding, self.input_data))
                inputs = tf.split( tf.nn.embedding_lookup(embedding, self.input_data)  , args.seq_length,1)
                inputs = [tf.squeeze(input_, [1]) for input_ in inputs]

        def loop(prev, _):
            prev = tf.matmul(prev, softmax_w) + softmax_b
            prev_symbol = tf.stop_gradient(tf.argmax(prev, 1))
            return tf.nn.embedding_lookup(embedding, prev_symbol)

        # yonghua
        # inputs, initial_state, cell, scope
        outputs, last_state = seq2seq.rnn_decoder(inputs, self.initial_state, cell, loop_function=loop if infer else None, scope='rnnlm')
        #output = tf.reshape(tf.concat(1, outputs), [-1, args.rnn_size])
        output = tf.reshape(tf.concat(outputs,1), [-1, args.rnn_size])
        self.logits = tf.matmul(output, softmax_w) + softmax_b
        self.probs = tf.nn.softmax(self.logits, name="prob_results")
        loss = seq2seq.sequence_loss_by_example([self.logits],
                [tf.reshape(self.targets, [-1])],
                [tf.ones([args.batch_size * args.seq_length])],
                args.vocab_size)
        self.cost = tf.reduce_sum(loss) / args.batch_size / args.seq_length
        self.final_state = last_state
        self.lr = tf.Variable(0.0, trainable=False,name="LR_")
        tvars = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.cost, tvars),
                args.grad_clip)
        optimizer = tf.train.AdamOptimizer(self.lr)
        self.train_op = optimizer.apply_gradients(zip(grads, tvars))

    def sample(self, sess, chars, vocab, num = 200, prime='The ', sampling_type=1):
        ifToRewrite = 0
        prime = prime.strip()
        ret = prime
        while True:
          state = sess.run(self.cell.zero_state(1, tf.float32))
          if ifToRewrite == 0:
              try:
                prime = prime.strip().decode("gbk")
              except:
                exit()

          ifToRewrite = 0
          for char in prime[:-1]:
              x = np.zeros((1, 1))
              if char not in vocab:
                continue
              try:
                x[0, 0] = vocab[char]
              except:
                continue
              feed = {self.input_data: x, self.initial_state:state}
              [state] = sess.run([self.final_state], feed)
          def weighted_pick(weights):
              t = np.cumsum(weights)
              s = np.sum(weights)
              return(int(np.searchsorted(t, np.random.rand(1)*s)))
        
          #sys.stdout.write("%s" % prime) # beginning
          if len(prime) == 0:
            exit()
          char = prime[-1]
          
          numOfChunk = 0
          LengthOfSingleSentence = 0
          completed = 0
          for n in range(num):
            x = np.zeros((1, 1))
            if char not in vocab:
              continue
            try:
              x[0, 0] = vocab[char]
            except:
              continue

            feed = {self.input_data: x, self.initial_state:state}
            [probs, state] = sess.run([self.probs, self.final_state], feed)
        
            p = probs[0]
            if sampling_type == 0:
              sample = np.argmax(p)
            elif sampling_type == 2:
              if char == ' ':
                sample = weighted_pick(p)
              else:
                sample = np.argmax(p)
            else: # sampling_type == 1 default:
              sample = weighted_pick(p)
            pred = chars[sample]
            ret += pred.encode("gbk")
            char = pred
            LengthOfSingleSentence += 1
            if char.encode("gbk") == "��":
                numOfChunk += 1
            char_ = char.encode("gbk")
            if char_ == "��" or char_ == "��" or char_ == "��":
                LengthOfSingleSentence = 0
            if LengthOfSingleSentence > 10:
                ifToRewrite = 1
                completed = 0
                break
            if numOfChunk > 2:
                completed = 1
                break

          #sys.stdout.write("\n")
          if completed == 1:
              ret += "\n"
              break
              #sys.stdout.write(">%s" % ret)
        return ret
