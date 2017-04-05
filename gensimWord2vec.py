# coding:utf-8

import os
from gensim.models import Word2Vec
import logging

FENCI_TRAIN_PATH = '../data/fenci_train.dat'
FENCI_VALI_PATH = '../data/fenci_vali.dat'
FENCI_TEST_PATH = '../data/fenci_test.dat'

MODEL_SAVED_PATH = '../models/gesimWord2vec_train.model'

def getSetences(filepath):
    ss = []
    for line in open(filepath, 'r'):
        ss.append(line.split(' '))
    return ss


def train(filepath):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    ss = getSetences(filepath)
    model = Word2Vec(ss, size=200)  # 训练skip-gram模型; 默认window=5
    model.save(MODEL_SAVED_PATH)
    print 'model saved.'

def checkmodel(model, word):
    # res = model.most_similar(positive=['中国', '纽约'], negative=['北京'])
    res = model.most_similar(word)
    print 'keyword: ', word, '\nmost similar:'
    for item in res:
        print item[0], item[1]

if __name__ == '__main__':
    # train(FENCI_TRAIN_PATH)
    model = Word2Vec.load(MODEL_SAVED_PATH)
    checkmodel(model, '癌症')