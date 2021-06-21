from numpy import *
import numpy as np
import time
import matplotlib.pyplot as plt

# 计算每个文档的关键词和词频
# 关键词统计和词频统计，以列表形式返回
def Count(resfile):
    t = {}
    infile = open(resfile, 'r', encoding='utf-8')
    i = 0
    f = infile.readlines()
    count = len(f)
    # print(count)
    infile.close()
    s = open(resfile, 'r', encoding='utf-8')
    while i < count:
        line = s.readline()
        line = line.rstrip('\n')
        # print(line)
        words = line.split(" ")
        #   print(words)
        for word in words:
            if word != "" and t.__contains__(word):
                num = t[word]
                t[word] = num + 1
            elif word != "":
                t[word] = 1
        i = i + 1
    # 按键值降序
    dic = sorted(t.items(), key=lambda t: t[1], reverse=True)
    s.close()
    # 返回的是一篇文档的词项统计表，形式为[(word:出现次数)]
    return dic


def readfile():
    f = open("res.txt", "w", encoding="utf-8")
    # mergeword 用来记录所有文档的词项集合，不重复，其长度是用来作为文档向量维度
    mergeword = []
    everyDocumentDict = []
    for i in range(1, 501):
        filedir = "AnalyzeTxtC\BBS_" + str(i) + "_C.txt"
        # 将每个文档的字典写入res.txt中
        dict = Count(filedir)
        # everyDocumentDict记录的是每篇文档的词项统计
        everyDocumentDict.append(dict)
        # print(type(dict))
        for j in range(len(dict)):
            if dict[j][0] not in mergeword:
                mergeword.append(dict[j][0])
    f.close()
    # 返回文档集的词项集
    return mergeword, everyDocumentDict


# 现在有了500个文档的总关键词和每篇文档的词项统计，所以我们现在要做的是将每篇文档向量化，维度是len(mergeword)
# 注意EveDocCount的结构是[[(),()],[(),()]]，里面记录的列表是每个文档的词项统计，而括号里面的是keyword:词频
def VectorEveryDoc(EveDocCount, mergeword):
    print("-------------------文档向量化开始操作-----------------")
    # vecOfDoc列表记录的是每篇文档向量化后的向量列表，共有500个元素
    vecOfDoc = []
    # vecDoc列表记录的是一篇文档的向量模型，向量化后添加到vecOfDoc
    vectorLenth = len(mergeword)
    # 下面开始将500文档向量化
    i = 0
    while i < 500:
        # EveDocCount[i]记录的是第几篇文档的词项统计
        vecDoc = [0] * vectorLenth
        # 测试是正确的
        # print(EveDocCount[i])
        for ch in range(len(EveDocCount[i])):
            # termFrequence 是词项对应的频数
            termFrequence = EveDocCount[i][ch][1]
            # keyword是词项
            keyword = EveDocCount[i][ch][0]
            # 下面开始具体的向量化
            j = 0
            while j < vectorLenth:
                if keyword == mergeword[j]:
                    # 这里是J 而不是 I ,写错了就很容易出错了
                    vecDoc[j] = termFrequence
                    break
                else:
                    j = j + 1
        vecOfDoc.append(vecDoc)
        i = i + 1
    # 返回500个文档的文档向量
    print("-------------------文档向量化操作结束-----------------")
    return vecOfDoc


# 计算余弦距离
def CalConDis(v1, v2):
    lengthVector = len(v1)
    # 计算出两个向量的乘积
    # 将v2变换，转置矩阵v2
    v2s = v2.T
    B = np.dot(v1, v2s)
    # 计算两个向量的模的乘积
    v1s = v1.T
    A1 = np.dot(v1, v1s)
    A2 = np.dot(v2, v2s)
    A = math.sqrt(A1) * math.sqrt(A2)
    # print('相似度 = ' + str(float(B) / A))
    resdis = format(float(B) / A, ".3f")
    return float(resdis)


# 随机选取中心点,dateSet是m * n矩阵，K是要指定的聚类的个数
def createRandomCent(dateSet, k):
    # 返回整个矩阵的列的列数
    n = np.shape(dateSet)[1]
    # 创建一个k * n 的零矩阵
    centroids = np.mat(np.zeros((k, n)))
    # 随机产生k个中心点
    for j in range(n):
        minJ = min(dateSet[:, j])
        rangeJ = float(max(dateSet[:, j]) - minJ)
        centroids[:, j] = np.mat(minJ + rangeJ * np.random.rand(k, 1))
    # 返回随机产生的k个中心点
    return centroids



# show your cluster only available with 2-D data
# centroids为k个类别，其中保存着每个类别的质心
# clusterAssment为样本的标记，第一列为此样本的类别号，第二列为到此类别质心的距离
def showCluster(dataSet, k, centroids, clusterAssment):
    numSamples, dim = dataSet.shape
    if dim != 2:
        print("Sorry! I can not draw because the dimension of your data is not 2!")
        return 1

    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    if k > len(mark):
        print("Sorry! Your k is too large! please contact wojiushimogui")
        return 1

        # draw all samples
    for i in range(numSamples):
        markIndex = int(clusterAssment[i, 0])  # 为样本指定颜色
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])

    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    # draw the centroids
    for i in range(k):
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize=12)

    plt.show()


countclu = 1
# 具体的Kmeans算法实现
# dateset是指500个文档的向量集合(500 * length),dis用的是余弦距离,k是给定的k个聚类中心,createCent是随机生成的K个初始中心
def dfdocKmeansCluster(dateset, k, discos=CalConDis, createCent=createRandomCent):
    # docCount 记录的总共有多少个样本,既矩阵的行数
    docCount = np.shape(dateset)[0]
    # 在构建一个500 * 2的0矩阵,用来存放聚类信息
    docCluster = np.mat(np.zeros((docCount, 2)))

    # 初始化K个聚类中心
    centerOfCluster = createCent(dateset, k)
    # clusterFlag用来判定聚类是否结束
    clusterFlag = True
    while clusterFlag:
        clusterFlag = False
        for each in range(docCount):
            # 将最大余弦距离初始化成一个负数
            maxCosDis = -100
            # 文档索引
            minIndex = -1
            # 找到每篇文档距离最近的中心
            for i in range(k):
                # 计算每个文档到中心点的余弦相似度,
                global countclu
                countclu = countclu + 1
                print("已经聚类第" + str(countclu) + "次")
                distcosOfDocToDoccenter = discos(centerOfCluster[i, :], dateset[each, :])
                # 选择余弦距离最大的一个中心
                if distcosOfDocToDoccenter > maxCosDis:
                    maxCosDis = distcosOfDocToDoccenter
                    minIndex = i
            if docCluster[each, 0] != minIndex:
                # 如果没到最优方案则继续聚类
                clusterFlag = True
            # 第1列为所属中心，第2列为余弦距离
            docCluster[each, :] = minIndex, maxCosDis
        # 打印随机产生的中心点
        print(centerOfCluster)

        # 更改聚类中心点
        for cent in range(k):
            ptsInClust = dateset[np.nonzero(docCluster[:, 0].A == cent)[0]]
            centerOfCluster[cent, :] = np.mean(ptsInClust, axis=0)
    # 返回K个中心点,
    return centerOfCluster, docCluster


if __name__ == '__main__':
    # 测试文档集关键词是否正确
    mergeword, eveKeywordOfCount = readfile()
    resultVec = VectorEveryDoc(eveKeywordOfCount, mergeword)
    vecData = np.array(resultVec)
    centroids, clusterAssment = kmeans(vecData, 20)
    print(centroids)
    print(clusterAssment)
    #showCluster(vecData, 20, centroids, clusterAssment)
