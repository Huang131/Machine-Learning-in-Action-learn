"""
@Descripttion: 可视化决策树
@version: 0.0.1
@Author: Huang
@dev: python3 vscode
@Date: 2019-10-26 17:19:42
@LastEditors: Huang
@LastEditTime: 2019-10-26 17:19:49
"""

from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from trees import *


def getNumLeafs(myTree):
    """
    [summary]:获取决策树叶子结点的数目
    
    Arguments:
        myTree  -- 决策树
    
    Returns:
         numLeafs -- 决策树的叶子结点的数目
    """
    numLeafs = 0  # 初始化叶子
    firstStr = next(iter(myTree))
    secondDict = myTree[firstStr]  # 获取下一组字典
    for key in secondDict.keys():
        # 测试该结点是否为字典，如果不是字典，代表此结点为叶子结点
        if type(secondDict[key]).__name__ == "dict":
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs


def getTreeDepth(myTree):
    """
    [summary]:获取决策树的层数
    
    Arguments:
        myTree  -- 决策树
    
    Returns:
        maxDepth - 决策树的层数
    """
    maxDepth = 0  # 初始化决策树的深度
    firstStr = next(iter(myTree))
    secondDict = myTree[firstStr]  # 获取下一个字典
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == "dict":
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
            maxDepth = max(thisDepth, maxDepth)
    return maxDepth


def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    """
    [summary]:绘制节点
    
    Arguments:
        nodeTxt -- 节点名
        centerPt -- 文本位置
        parentPt -- 标注的箭头位置
        nodeType -- 节点格式
    """
    arrow_args = dict(arrowstyle="<-")  # 定义箭头格式
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)  # 绘制中文字体
    createPlot.ax1.annotate(
        nodeTxt,
        xy=parentPt,
        xycoords="axes fraction",
        xytext=centerPt,
        textcoords="axes fracion",
        va="center",
        ha="center",
        bbox=nodeType,
        arrowprops=arrow_args,
        FontProperties=font,
    )


def plotMidText(cntrPt, parentPt, txtString):
    """
    [summary]:标注有向边属性值
    
    Arguments:
        cntrPt {[type]} -- 用于计算标注位置
        parentPt {[type]} -- 用于计算标注位置
        txtString {[type]} -- 标注的内容
    """
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]  # 计算标注位置
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)


def plotTree(myTree, parentPt, nodeTxt):
    """
    [summary]:绘制决策树
    
    Arguments:
        myTree {[type]} --决策树(字典)
        parentPt {[type]} -- 标注的内容
        nodeTxt {[type]} -- 结点名
    """
    decisionNode = dict(boxstyle="sawtooth", fc="0.8")  # 设置结点格式
    leafNode = dict(boxstyle="round4", fc="0.8")  # 设置叶结点格式
    numLeafs = getNumLeafs(myTree)  # 获取决策树叶结点数目，决定了树的宽度
    depth = getTreeDepth(myTree)  # 获取决策树层数
    firstStr = next(iter(myTree))  # 下个字典
    cntrPt = (
        plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW,
        plotTree.yOff,
    )  # 中心位置
    plotMidText(cntrPt, parentPt, nodeTxt)  # 标注有向边属性值
    plotNode(firstStr, cntrPt, parentPt, decisionNode)  # 绘制结点
    secondDict = myTree[firstStr]  # 下一个字典，也就是继续绘制子结点
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD  # y偏移
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == "dict":  # 测试该结点是否为字典，如果不是字典，代表此结点为叶子结点
            plotTree(secondDict[key], cntrPt, str(key))  # 不是叶结点，递归调用继续绘制
        else:  # 如果是叶结点，绘制叶结点，并标注有向边属性值
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD


def createPlot(inTree):
    """
    [summary]:创建绘制面板
    
    Arguments:
        inTree  -- 决策树(字典)
    """
    fig = plt.figure(1, facecolor="white")  # 创建fig
    fig.clf()  # 清空fig
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)  # 去掉x、y轴
    plotTree.totalW = float(getNumLeafs(inTree))  # 获取决策树叶结点数目
    plotTree.totalD = float(getTreeDepth(inTree))  # 获取决策树层数
    plotTree.xOff = -0.5 / plotTree.totalW
    plotTree.yOff = 1.0
    # x偏移
    plotTree(inTree, (0.5, 1.0), "")  # 绘制决策树
    plt.show()  # 显示绘制结果


if __name__ == "__main__":
    dataSet, labels = createDataSet()
    featLabels = []
    myTree = createTree(dataSet, labels, featLabels)
    print(myTree)
    createPlot(myTree)
