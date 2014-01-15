import os
import math
import matplotlib.pyplot as plt

def createDataSet():  
    dataSet = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]  
    features = ['no surfacing','flippers']  
    return dataSet,features 

def treeGrowth(dataSet,features):  
    classList = [example[-1] for example in dataSet]  
    if classList.count(classList[0])==len(classList):  
        return classList[0]  
    if len(dataSet[0])==1:# no more features  
        return classify(classList)  
  
    bestFeat = findBestSplit(dataSet)#bestFeat is the index of best feature  
    bestFeatLabel = features[bestFeat]  
    myTree = {bestFeatLabel:{}}  
    featValues = [example[bestFeat] for example in dataSet] 
    uniqueFeatValues = set(featValues)  
    del (features[bestFeat])  
    for values in uniqueFeatValues:  
        subDataSet = splitDataSet(dataSet,bestFeat,values)  
        myTree[bestFeatLabel][values] = treeGrowth(subDataSet,features)  
    return myTree

def classify(classList):  
    ''''' 
    find the most in the set 
    '''  
    classCount = {}  
    for vote in classList:  
        if vote not in classCount.keys():  
            classCount[vote] = 0  
        classCount[vote] += 1  
    sortedClassCount = sorted(classCount.iteritems(),key = operator.itemgetter(1),reverse = True)  
    return sortedClassCount[0][0]  

def findBestSplit(dataset):  
    numFeatures = len(dataset[0])-1
    baseEntropy = calcShannonEnt(dataset)  
    bestInfoGain = 0.0  
    bestFeat = -1  
    for i in range(numFeatures):  
        featValues = [example[i] for example in dataset]  
        uniqueFeatValues = set(featValues)
        newEntropy = 0.0  
        for val in uniqueFeatValues:  
            subDataSet = splitDataSet(dataset,i,val)  
            prob = len(subDataSet)/float(len(dataset))  
            newEntropy += prob*calcShannonEnt(subDataSet)  
        if(baseEntropy - newEntropy)>bestInfoGain:  
            bestInfoGain = baseEntropy - newEntropy  
            bestFeat = i  
    return bestFeat  

def splitDataSet(dataset,feat,values):
    retDataSet = []  
    for featVec in dataset: 
        if featVec[feat] == values:  
            reducedFeatVec = featVec[:feat]
            reducedFeatVec.extend(featVec[feat+1:])  
            retDataSet.append(reducedFeatVec)  
    return retDataSet  


def calcShannonEnt(dataset):  
    numEntries = len(dataset)  
    labelCounts = {}  
    for featVec in dataset:  
        currentLabel = featVec[-1]
        
        if currentLabel not in labelCounts.keys():  
            labelCounts[currentLabel] = 0  
        labelCounts[currentLabel] += 1  
    shannonEnt = 0.0  

    #print "labelcounts is:"
    #print labelCounts
    for key in labelCounts:  
        prob = float(labelCounts[key])/numEntries  
        if prob != 0:  
            shannonEnt -= prob*math.log(prob,2)  
    return shannonEnt  

def predict(tree,newObject):  
    while isinstance(tree,dict):  
        key = tree.keys()[0]  
        tree = tree[key][newObject[key]]  
    return tree

def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    createPlot.axl.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',
    xytext=centerPt,textcoords='axes fraction',
    va="center",ha="center",bbox=nodeType,arrowprops=arrow_args)

#def createPlot():
#    fig=plt.figure(1,facecolor='white')
#    fig.clf()
#    createPlot.axl=plt.subplot(111,frameon=False)
#    plotNode('a desion node',(0.5,0.1),(0.1,0.5),deccisionNode)
#    plotNode('a leaf node',(0.8,0.1),(0.3,0.8),leafNode)
#    plt.show()   

def getNumLeafs(myTree):
    numLeafs = 0
    firstStr=myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs+=1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth = 1+ getTreeDepth(secondDict[key])
        else:
            thisDepth=1
        if thisDepth>maxDepth:maxDepth=thisDepth
    return maxDepth

def plotMidText(cntrPt , parentPt , txtString):
    xMid = (parentPt[0] > cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.axl.text(xMid, yMid, txtString)

def plotTree(myTree , parentPt , nodeTxt):
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = myTree.keys()[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff)
    plotMidText(cntrPt , parentPt , nodeTxt)
    plotNode(firstStr, cntrPt , parentPt , decisionNode)
    secondDict =myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key] , cntrPt , str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key] , (plotTree.xOff , plotTree.yOff),cntrPt , leafNode)
            plotMidText((plotTree.xOff , plotTree.yOff) , cntrPt , str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

def createPlot(inTree):
    fig = plt.figure(1 , facecolor='white')
    fig.clf()
    axprops = dict(xticks=[] , yticks=[])
    createPlot.axl = plt.subplot(111 , frameon=False , **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
    plotTree(inTree , (0.5 , 1.0),'')
    plt.show()
    
if __name__ == '__main__':
    dataset,features = createDataSet()  
    #rint "shannon is"
    #print 
    calcShannonEnt(dataset)
    
    tree = treeGrowth(dataset,features) 
    print tree  
    #print predict(tree,{'no surfacing':1,'flippers':1})  
    #print predict(tree,{'no surfacing':1,'flippers':0})  
    #print predict(tree,{'no surfacing':0,'flippers':1})  
    #print predict(tree,{'no surfacing':0,'flippers':0})  
    
    #draw a tree
    decisionNode=dict(boxstyle="sawtooth",fc="0.8")
    leafNode = dict(boxstyle="round4",fc="0.8")
    arrow_args=dict(arrowstyle="<-")
    createPlot(tree)



