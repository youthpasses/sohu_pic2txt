# coding:utf-8

import os

MATCHFILE_PATH = '../data/trainMatching.txt'


def check():
    unmatchs = []
    for line in open(MATCHFILE_PATH, 'r'):
        line0 = line
        line.strip()
        line.replace(' ', '\t')
        line = line.split('\t')
        if len(line) > 2:
            print 'error: ', line0
            unmatchs.append(line0)
        name1 = line[0].split('.')[0]
        name2 = line[1].split('.')[0]
        print name1, name2
        if name1 != name2:
            print 'error: ', line0
            unmatchs.append(line0)
    if len(unmatchs) == 0:
        print 'no unmatched.'
    else:
        print len(unmatchs), 'unmatched. list:'
        for line in unmatchs:
            print line

if __name__ == "__main__":
    # check()
    for line in open(MATCHFILE_PATH, 'r'):
        print line