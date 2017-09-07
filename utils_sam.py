import codecs
import os
import collections
from six.moves import cPickle
import numpy as np
import re

isAlphaNum = re.compile(r'^[0-9a-zA-Z]+$')

def strQ2B(ustring):
        rstring = ""
        #ustring = ustring.decode("utf8")
        ustring = ustring.decode("gb18030")
        for uchar in ustring:
                inside_code=ord(uchar)
                if inside_code==0x3000:
                        inside_code=0x0020
                else:
                        inside_code-=0xfee0
                if inside_code<0x0020 or inside_code>0x7e: 
                        rstring += uchar
                        continue
                rstring += unichr(inside_code)
        return rstring.encode("gb18030")

class TextLoader():
    #def __init__(self, data_dir, batch_size, seq_length, encoding='gbk'):
    def __init__(self, data_dir, batch_size, seq_length, encoding='utf-8'):
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.encoding = encoding
        print("data_dir : %s" , data_dir)
        #input_file = os.path.join(data_dir, "train.dat")
        #input_file = os.path.join(data_dir, "input.txt")
        #input_file = os.path.join(data_dir, "poem.170816.gbk.txt.content.utf8")
        input_file = os.path.join(data_dir, "poem.txt.utf8")
        #input_file = os.path.join(data_dir, "train.data.total.format.utf8")
        vocab_file = os.path.join(data_dir, "vocab.pkl")
        tensor_file = os.path.join(data_dir, "data.npy")
        print("input_file : %s" , input_file)

        if not (os.path.exists(vocab_file) and os.path.exists(tensor_file)):
            print("reading text file")
            self.preprocess(input_file, vocab_file, tensor_file)
        else:
            print("loading preprocessed files")
            self.load_preprocessed(vocab_file, tensor_file)
        self.create_batches()
        self.reset_batch_pointer()

    ## Process the input data into vocab && tensor file.
    def preprocess(self, input_file, vocab_file, tensor_file):
        print("[preprocess] input_file : %s" , input_file)
        print("self.encoding:")
        print(self.encoding)
        data = []
        with codecs.open(input_file, "r", encoding=self.encoding) as f:
          for line in f.readlines():
            line = line.strip()
            arr = line.split(" ")
            for i in range(0,len(arr)):
#              banjiao = strQ2B(arr[i])
#              if isAlphaNum.match(banjiao):
#                null = 1
#              else:
                data.append(arr[i])
            #data = f.read()
            #for w in data:   ## Here a single character is the content of w.
            #  print(w)
        #print ("------------------------haha")
        counter = collections.Counter(data)
        count_pairs = sorted(counter.items(), key=lambda x: -x[1])
        self.chars, _ = zip(*count_pairs)
        self.vocab_size = len(self.chars)
        self.vocab = dict(zip(self.chars, range(len(self.chars))))
        with open(vocab_file, 'wb') as f:
            cPickle.dump(self.chars, f)
        self.tensor = np.array(list(map(self.vocab.get, data)))
        np.save(tensor_file, self.tensor)

    def load_preprocessed(self, vocab_file, tensor_file):
        with open(vocab_file, 'rb') as f:
            self.chars = cPickle.load(f)
        self.vocab_size = len(self.chars)
        self.vocab = dict(zip(self.chars, range(len(self.chars))))
        self.tensor = np.load(tensor_file)
        self.num_batches = int(self.tensor.size / (self.batch_size *
                                                   self.seq_length))

    def create_batches(self):
        self.num_batches = int(self.tensor.size / (self.batch_size *
                                                   self.seq_length))

        # When the data (tensor) is too small, let's give them a better error message
        if self.num_batches==0:
            assert False, "Not enough data. Make seq_length and batch_size small."

        self.tensor = self.tensor[:self.num_batches * self.batch_size * self.seq_length]
        xdata = self.tensor
        ydata = np.copy(self.tensor)
        ydata[:-1] = xdata[1:]
        ydata[-1] = xdata[0]
        self.x_batches = np.split(xdata.reshape(self.batch_size, -1), self.num_batches, 1)
        self.y_batches = np.split(ydata.reshape(self.batch_size, -1), self.num_batches, 1)


    def next_batch(self):
        x, y = self.x_batches[self.pointer], self.y_batches[self.pointer]
        self.pointer += 1
        return x, y

    def reset_batch_pointer(self):
        self.pointer = 0
