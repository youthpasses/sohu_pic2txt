# coding:utf-8
import os
import shutil
from PIL import Image
import imghdr

TRAIN_PIC = 'train_pic'
VALI_PIC = 'vali_pic'
TEST_PIC = 'test_pic'
PRE_DIR = '../data'


def imageIsGood(imagepath):
    houzhui = imghdr.what(imagepath)
    if not houzhui or houzhui == 'gif':
        return False
    else:
        img = Image.open(imagepath)
        if img.size[0] < 150 and img.size[1] < 150:
            return False
    return True

def mkdir(data_dir):
    picdir = ''
    notxt = True
    if data_dir == TRAIN_PIC:
        picdir = '../dropeddata/train_pic'
        notxt = False
    elif data_dir == VALI_PIC:
        picdir = '../dropeddata/vali_pic'
    else:
        picdir = '../dropeddata/test_pic'

    if not os.path.exists(picdir):
        os.makedirs(picdir)
    print '1'
    if not notxt:
        print '2'
        txtdir = '../dropeddata/train_txt'
        if not os.path.exists(txtdir):
            print '3'
            os.mkdir(txtdir)
            print '4'

def handleBadData(data_dir, imagename):
    imagepath = os.path.join(os.path.join(PRE_DIR, data_dir), imagename)
    picdir = ''
    notxt = True
    if data_dir == TRAIN_PIC:
        picdir = '../dropeddata/train_pic'
        notxt = False
    elif data_dir == VALI_PIC:
        picdir = '../dropeddata/vali_pic'
    else:
        picdir = '../dropeddata/test_pic'
    newpath = os.path.join(picdir, imagename)
    shutil.move(imagepath, newpath)

    if not notxt:
        txtdir = '../data/train_txt'
        txtname = imagename.split('.')[0] + '.txt'
        txtpath = os.path.join(txtdir, txtname)
        newTxtpath = os.path.join('../dropeddata/train_txt', txtname)
        shutil.move(txtpath, newTxtpath)


def check(data_dir):
    mkdir(data_dir)
    imagedir = os.path.join(PRE_DIR, data_dir)
    imagenames = os.listdir(imagedir)
    imagenames.sort()
    for imagename in imagenames:
        imagepath = os.path.join(imagedir, imagename)
        if not imageIsGood(imagepath):
            print 'bad: ', imagepath
            handleBadData(data_dir, imagename)



if __name__ == '__main__':
    check(TRAIN_PIC)
    check(VALI_PIC)
    check(TEST_PIC)
