# coding:utf-8

import gensim
from gensim import corpora
import time
import os
import shutil

FENCI_TEST_PATH = '../data/fenci_test.dat'
FENCI_TRAIN_PATH = '../data/fenci_train.dat'
FENCI_VALI_PATH = '../data/fenci_vali.dat'

TRAIN_PIC_DIR = '../data/train_pic'
TRAIN_TXT_DIR = '../data/train_txt'

NUM_TOPICS = 20
PASSES = 5
CHUNKSIZE = 5000


def getCorpus(fencipath):
    lines = []
    for line in open(fencipath):
        lines.append(line.strip().split(' '))
    id2word = corpora.Dictionary(lines)
    id2word.filter_extremes(no_below=10, no_above=0.1)
    corpus = [id2word.doc2bow(line) for line in lines]
    print 'handle data over.'
    return id2word, corpus



def train(fencipath):
    saved_dir = ''
    if fencipath == FENCI_TEST_PATH:
        saved_dir = '../models/gensim_LDA_test'
    elif fencipath == FENCI_VALI_PATH:
        saved_dir = '../models/gensim_LDA_vali'
    else :
        saved_dir = '../models/gensim_LDA_train'
    if not os.path.exists(saved_dir):
        os.makedirs(saved_dir)

    beginT = time.time()
    id2word, corpus = getCorpus(fencipath)
    id2word.save_as_text(os.path.join(saved_dir, 'id2word.txt'))

    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=NUM_TOPICS, iterations=100, update_every=1, chunksize=CHUNKSIZE, passes=PASSES)
    lda_model.save(os.path.join(saved_dir, 'gensimlda_topic' + str(NUM_TOPICS) + '.model'))
    lda_model.print_topics(10)
    print 'finish: ', time.time()
    print 'duration: ', time.time() - beginT

def check():
    model = gensim.models.LdaModel.load('../models/gensim_LDA_train/gensimlda_topic20.model')
    model.print_topics(50)
    line = open(FENCI_VALI_PATH).readlines()[130]
    print line
    id2word = corpora.Dictionary.load_from_text('../models/gensim_LDA_train/id2word.txt')
    bow = id2word.doc2bow(line.split(' '))
    res = model.get_document_topics(bow)
    for id, value in res:
        print id, value

def classify(modelpath):
    model = gensim.models.ldamodel.LdaModel.load(modelpath)
    show_topics = model.show_topics(num_topics=100)
    for id, topic in show_topics:
        print id, topic

    # mk dir
    for id, topic in show_topics:
        picdir = '../data/train_topics_' + str(NUM_TOPICS) + '/' + str(id) + '/pic'
        txtdir = '../data/train_topics_' + str(NUM_TOPICS) + '/' + str(id) + '/txt'
        if not os.path.exists(picdir):
            os.makedirs(picdir)
        if not os.path.exists(txtdir):
            os.makedirs(txtdir)

    txtnames = os.listdir(TRAIN_TXT_DIR)
    id2word = corpora.Dictionary.load_from_text('../models/gensim_LDA_train/id2word.txt')
    i = 0
    for line in open(FENCI_TRAIN_PATH):
        toptopics = model.get_document_topics(id2word.doc2bow(line.split(' ')))
        topic_id = 0
        topic_p = 0
        for id, p in toptopics:
            if p > topic_p:
                topic_id = id
                topic_p = p
        desTxtDir = '../data/train_topics_' + str(NUM_TOPICS) + '/' + str(topic_id) + '/txt'
        desPicDir = '../data/train_topics_' + str(NUM_TOPICS) + '/' + str(topic_id) + '/pic'
        txtname = txtnames[i]
        picname = txtname.split('.')[0] + '.'
        txtPath = os.path.join(TRAIN_TXT_DIR, txtname)
        if os.path.exists(os.path.join(TRAIN_PIC_DIR, picname + 'JPEG')):
            picname = picname + 'JPEG'
        elif os.path.exists(os.path.join(TRAIN_PIC_DIR, picname + 'jpg')):
            picname = picname + 'jpg'
        elif os.path.exists(os.path.join(TRAIN_PIC_DIR, picname + 'jpeg')):
            picname = picname + 'jpeg'
        elif os.path.exists(os.path.join(TRAIN_PIC_DIR, picname + 'JPG')):
            picname = picname + 'JPG'
        elif os.path.exists(os.path.join(TRAIN_PIC_DIR, picname + 'png')):
            picname = picname + 'png'
        elif os.path.exists(os.path.join(TRAIN_PIC_DIR, picname + 'PNG')):
            picname = picname + 'PNG'
        picPath = os.path.join(TRAIN_PIC_DIR, picname)
        desTxtPath = os.path.join(desTxtDir, txtname)
        desPicPath = os.path.join(desPicDir, picname)
        shutil.copy(txtPath, desTxtPath)
        shutil.copy(picPath, desPicPath)
        print i, '\t', picPath, ' =====> ', desPicPath
        i = i + 1



if __name__ == '__main__':
    import logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # train(FENCI_TRAIN_PATH)
    check()
    # classify('../models/gensim_LDA_train/gensimlda_topic20.model')