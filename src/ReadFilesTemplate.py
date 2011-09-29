# coding: utf-8
#ファイルを読み込んで、何かをするためのひな型

import glob

for filepath in glob.glob('/Documents and Settings/Administrator/My Documents/*.txt'):
    file = open(filepath, 'r')
    for line in file:
        #ここに処理を実装していく
        print line
