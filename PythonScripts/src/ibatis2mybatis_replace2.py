# coding: utf-8

#指定フォルダ配下のxmlファイルに対する置換

import glob
import re

#編集対象のxmlファイルまでのパス
daoPath = '/Program Files/eclipse/workspace/pdnMyBatis/src/main/com/fujitsu/pdn/process/dao/'

# xmlファイルを順次読み書きモードで開く
for filepath in glob.glob(daoPath + '*.xml'):
    daoFile = open(filepath, 'r+')
    newLines = []
    isModified = False
    iterateProcessStatus = ''
    for line in daoFile:
        newLine = line
        newLine = newLine.replace('type="pre"', 'order="BEFORE"')
        newLine = newLine.replace('type="post"', 'order="AFTER"')
        newLine = newLine.replace('remapResults="true"', 'useCache="false"')

        m = re.search(r'<is(Not)?Null', newLine)
        if m != None:
            startTag = m.group()
            newLine = newLine.replace(startTag, '<if')
            propertyAttr = re.search(r'property="\w+"', newLine).group()
            testAttr = propertyAttr.replace('property', 'test')
            if 0 <= startTag.find('Not'):
                comp = ' != '
            else:
                comp = ' == '
            testAttr = testAttr.rstrip('"') + comp + 'null"'
            newLine = newLine.replace(propertyAttr, testAttr)
        newLine = re.compile('</is(Not)?Null>').sub('</if>', newLine)

        m = re.search(r'<is(Not)?Equal', newLine)
        if m != None:
            startTag = m.group()
            newLine = newLine.replace(startTag, '<if')
            propertyAttr = re.search(r'property="\w+"', newLine).group()
            compareValueAttr = re.search(r'compareValue="\w+"', newLine).group()
            compareValue = compareValueAttr.replace('compareValue=', '').strip('"')
            if compareValue != 'null' and compareValue != 'true' and compareValue != 'false':
                compareValue = '\'' + compareValue + '\''
            testAttr = propertyAttr.replace('property', 'test')
            if 0 <= startTag.find('Not'):
                comp = ' != '
            else:
                comp = ' == '
            testAttr = testAttr.rstrip('"') + comp + compareValue + '"'
            newLine = newLine.replace(propertyAttr, testAttr)
            newLine = newLine.replace(' ' + compareValueAttr, '')
        newLine = re.compile('</is(Not)?Equal>').sub('</if>', newLine)

        if 0 <= newLine.find('<iterate'):
            newLine = newLine.replace('<iterate', '<foreach item="str"')
            iterateProcessStatus = 'startTag'
        if iterateProcessStatus == 'startTag':
            if 0 <= newLine.find('property='):
                index = newLine.find('property="') + len('property="')
                propertyName = newLine[index : newLine.find('"', index)]
            newLine = newLine.replace('property=', 'collection=')
            newLine = newLine.replace('conjunction=', 'separator=')
            if 0 <= newLine.find('>'):
                iterateProcessStatus = 'children'
        if iterateProcessStatus == 'children':
            newLine = newLine.replace('${' + propertyName + '[]}', '#{str}')
            if 0 <= newLine.find('</iterate>'):
                newLine = newLine.replace('</iterate>', '</foreach>')
                iterateProcessStatus = ''

        if newLine != line:
            isModified = True
        newLines.append(newLine)
    if isModified:
        daoFile.seek(0)               #ファイル書き換えに際し読み込み位置を先頭に戻し、
        daoFile.truncate(0)           #既存内容を消去
        daoFile.writelines(newLines)
        print daoFile.name
    daoFile.close()

