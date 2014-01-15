#! /usr/bin/env python
#coding=utf-8
#native bayes
# 朴素贝叶斯

from numpy import *

def loadDataSet():
    postingList=[['my' , 'dog' , 'has' , 'flea' ,'problems' , 'help' , 'please'] ,
    ['maybe' , 'not' , 'take' , 'him' ,'to' , 'dog' , 'park' , 'stupid'] ,
    ['my' , 'dalmation' , 'is' , 'so' , 'cute' , 111 , 'love I , I him 1'] ,
    ['stop' , 'posting' , 'stupid' , 'worthless' , 'garbage'] ,
    ['mr' , 'licks' , 'ate' , 'my' , 'steak' , 'how' , 'to' , 'stop' , ' him ' ],
    ['quit' , 'buying' , 'worthless' , 'dog' , 'food' , 'stupid']]

    classVec = [0 , 1 , 0 , 1 , 0 , 1] #1:代表侮辱性文字， 0代表正常言论
    return postingList , classVec

def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document) # 操作符|用于求两个集合的并集
    return list(vocabSet)

def setOfWords2Vec(vocabList , inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: 
            print "the word: is not in my Vocabulary!" %word
    return returnVec

def trainNBO(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    print "pAbusive is:"
    print trainCategory,numTrainDocs,pAbusive
    p0Num = zeros(numWords) 
    p1Num = zeros(numWords)
    p0Denom = 0.0; p1Denom = 0.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            #print "trainMatrix i is:"
            #print trainMatrix[i]
            p1Num += trainMatrix[i]
            #print p1Num
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
        #print p1Num
        p1vect = p1Num/p1Denom #change to log(),p1vect is a vector
        #print p1vect
        p0vect = p0Num/p0Denom #change to log()
    return p0vect ,p1vect , pAbusive


if __name__ == '__main__':
    listOPosts , listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    print myVocabList 
    #print len(myVocabList)
    #print setOfWords2Vec(myVocabList , listOPosts[0])
    #print setOfWords2Vec(myVocabList , listOPosts[3])
    trainMat= []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList , postinDoc))
    print trainMat
    print listClasses
    p0V ,p1V,pAb=trainNBO(trainMat , listClasses)
    print pAb,p0V,p1V