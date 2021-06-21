import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer("english") # 选择语言

# 创建停用词列表
def stopwordslist():
    stopword = set(stopwords.words('english'))
    # 添加部分符号
    for w in ['!', ',', '.', '?', '-s', '-ly', '</s>', 's', '“', '”', '’', '…', '...']:
        stopword.add(w)
    return stopword



# 对句子进行英文分词
def seg_depart(sentence):
    # 对文档中的每一行转换成小写并进行英文分词
    # print("正在分词")
    sentence_depart = word_tokenize(sentence.strip().lower())
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                # 去除部分单词后跟的...
                outstr += stemmer.stem(word.strip('…'))
                outstr += " "
    return outstr


if __name__ == '__main__':
    # 创建一个停用词列表
    stopwords = stopwordslist()
    for i in range(1, 601):
        # 给出文档路径
        filename = 'CrawlerSourceTxtE/Chapter_' + str(i) + '_Org.txt'
        outfilename = 'AnalyzeTxtE/Chapter_' + str(i) + '_E.txt'
        inputs = open(filename, 'r', encoding='UTF-8')
        outputs = open(outfilename, 'w+', encoding='UTF-8')
        # 将输出结果写入ou.txt中
        for line in inputs:

            line_seg = seg_depart(line)
            outputs.write(line_seg + '\n')
            # print("-----------正在分词和去停用词-----------")
        outputs.close()
        inputs.close()
        print('Chapter_' + str(i) + '_Org.txt删除停用词和分词,Porter Stemming操作成功！！！')
