# coding:utf-8

import os
import jieba

TRAIN_TXT_DIR = '../data/train_txt'
VALI_TXT_DIR = '../data/vali_txt'
TEST_TXT_DIR = '../data/test_txt'


# def dropStopWords(wordlist):


def getWordstring(txtpath, stopwordlist):
    f = open(txtpath, 'r')
    line = f.readlines()[0].strip()
    line = line.split(' ')[1:]
    line = ''.join(line)
    owordlist = jieba.cut(line, cut_all=False)
    wordlist = []
    for word in owordlist:
        word = word.strip().encode('utf-8')
        if word not in stopwordlist:
            wordlist.append(word)
    return ' '.join(wordlist)






def fenci(txt_dir):
    # stopword
    stopwordlist = open('../data/stop.txt', 'r').readlines()
    for i, word in enumerate(stopwordlist):
        stopwordlist[i] = word.strip()

    # file to save
    savedfilename = ''
    if txt_dir == TRAIN_TXT_DIR:
        savedfilename = '../data/fenci_train.dat'
    elif txt_dir == VALI_TXT_DIR:
        savedfilename = '../data/fenci_vali.dat'
    else:
        savedfilename = '../data/fenci_test.dat'
    f = open(savedfilename, 'a+')

    # read txt files
    txtnames = os.listdir(txt_dir)
    for i, txtname in enumerate(txtnames):
        txtpath = os.path.join(txt_dir, txtname)
        print i, txtpath
        s = getWordstring(txtpath, stopwordlist)
        s += '\n'
        f.write(s)
    f.close()




if __name__ == '__main__':
    # fenci(TRAIN_TXT_DIR)
    # fenci(VALI_TXT_DIR)
    # fenci(TEST_TXT_DIR)
    txtnames = os.listdir(TEST_TXT_DIR)
    print txtnames[:10]
