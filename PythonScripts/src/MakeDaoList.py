# coding: utf-8

#指定フォルダ配下のDAOインターフェースの型+変数名のリストを作る

import glob

#対象パス
daoPath = '/Program Files/eclipse/workspace/xxx/dao/'
#結果出力ファイルパス
resultFileName = 'daoTest.txt'

interfaceList = []
methodListMap = {}  #daoのインターフェース名とメソッドリストのマップ

# javaファイルを順次読みモードで開く
for filepath in glob.glob(daoPath + '*.java'):
    daoFile = open(filepath, 'r')
    isComment = False
    isBreakedLine = False
    interface = ''
    methodList = []
    for line in daoFile:
        line = line.strip('\n')

        #単行コメント
        if 0 <= line.find('//'):
            line = line[:line.find('//')]
        #コメントブロック開始
        if 0 <= line.find('/*'):
            isComment = True
            line = line[:line.find('/*')]
        #コメントブロック内
        if isComment:
            #コメントブロックの終端
            if 0 <= line.find('*/'):
                isComment = False
                line = line[line.find('*/') + len('*/'):]
            #コメントブロック継続
            else:
                continue

        #空行とクラス括弧行を除外
        if len(line.strip()) == 0 or line.strip() == '{' or line.strip() == '}':
            continue

        #インターフェース名を抽出
        if 0 <= line.find(' interface '):
            words = line.split()
            for i, word in enumerate(words):
                if word == 'interface':
                    interface = words[i + 1]
                    break
            continue
        #インターフェース定義内なのでメソッドを抽出
        if interface != '':
            #戻り値型除去
            if not(isBreakedLine) and 1 < len(line.split()):
                line = line.replace(line.split()[0], '', 1)
            #throws除去
            if 0 <= line.find('throws '):
                line = line.replace(line[line.find('throws '):line.rfind(';')], '')
            line = line.strip()

            #行を格納（改行されてる処理は1行に成形）
            if 0 < len(methodList) and isBreakedLine:
                methodList[len(methodList) - 1] += ' ' + line.strip()
            else:
                methodList.append(line)
            if line.strip().endswith(';'):
                isBreakedLine = False #改行されてない、または改行終了
            else:
                isBreakedLine = True #改行されてる

    daoFile.close()
    if interface != '':
        interfaceList.append(interface)
        methodListMap[interface] = methodList

#書き出しファイル指定
resultFile = open(resultFileName, 'w')
def printFile(s):
    print s
    resultFile.write(s + '\n')

#DAOインスタンス名を返す関数
def dao(interface):
    return interface[0].lower() + interface[1:len(interface) + 1]

#DAOインスタンス宣言
for interface in interfaceList:
    printFile('    @Autowired private ' + interface + ' ' + dao(interface) + ';')

printFile('')

#Testメソッド定義
for interface in interfaceList:
    for method in methodListMap[interface]:
        args = (method[method.find('(') + 1:method.find(')')])#引数部分を抽出
        #JavaDoc
        javaDocMethod = method.rstrip(';')
        for arg in args.split(','):
            if 0 == len(arg.strip()):
                continue #引数なし
            argName = arg.split()[1]
            javaDocMethod = javaDocMethod.replace(' ' + argName, '')
        printFile('    /**')
        printFile('     * {@link ' + interface + '#' + javaDocMethod + '}')
        printFile('     */')
        testMethod = 'test' + interface + method[:method.find('(')].replace(method[0],method[0].upper(),1)
        printFile('    @Test public void ' + testMethod + '() throws Exception {')
        #引数宣言を引数実体に書き換え
        for arg in args.split(','):
            if 0 == len(arg.strip()):
                continue #引数なし
            argType = arg.split()[0]
            argName = arg.split()[1]
            if argType == 'int' or argType == 'Integer': #int型引数
                method = method.replace(arg, '1')
            elif argType == 'long' or argType == 'Long': #long型引数
                method = method.replace(arg, 'new Long(1)')
            elif argType == 'boolean' or argType == 'Boolean': #Bool型引数
                method = method.replace(arg, 'true')
            elif argType == 'String': #String型引数
                method = method.replace(arg, '\"1\"')
            elif argType == 'Date': #Date型引数
                method = method.replace(arg, 'new Date()')
            else:#その他のクラスの引数
                printFile('        ' + argType + ' ' + argName + ' = new ' + argType + '();')
                method = method.replace(argType + ' ', '')
        printFile('        ' + dao(interface) + '.' + method)
        printFile('    }')

