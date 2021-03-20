# -*- coding: utf-8 -*-
from numpy import math
from pandas import DataFrame
import matplotlib.pyplot as plt

from readJSON import read

nasdata = read('nas100.json')



def show_relation(a, b):
    import statsmodels.api as smf  # 方法二
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression

    # est = smf.ols(formula='a ~ b', data=df).fit()  # 方法二
    # y_pred = est.predict(X)
    #
    # df['sales_pred'] = y_pred
    # print("sb66")
    #
    # print("回归结果jack", est.summary())  # 回归结果
    # print(est.params)  # 系数

    examdict = {"a": a, "b": b}

    examDf = DataFrame(examdict)

    rDf = examDf.corr()
    print(rDf)

    # plt.scatter(examDf.a, examDf.b, color='b', label="Exam Data")
    # plt.show()
    exam_X = examDf['a']
    exam_Y = examDf['b']

    X_train, X_test, Y_train, Y_test = train_test_split(exam_X, exam_Y, train_size=.6)
    # X_train为训练数据标签,X_test为测试数据标签,exam_X为样本特征,exam_y为样本标签，train_size 训练数据占比

    print("原始数据特征:", exam_X.shape,
          ",训练数据特征:", X_train.shape,
          ",测试数据特征:", X_test.shape)

    print("原始数据标签:", exam_Y.shape,
          ",训练数据标签:", Y_train.shape,
          ",测试数据标签:", Y_test.shape)

    plt.scatter(X_train, Y_train, color="blue", label="train data")
    # plt.scatter(X_test, Y_test, color="red", label="test data")  scatter

    model = LinearRegression()

    X_train = X_train.values.reshape(-1, 1)
    X_test = X_test.values.reshape(-1, 1)

    model.fit(X_train, Y_train)

    a = model.intercept_  # 截距

    b = model.coef_  # 回归系数

    print("最佳拟合线:截距", a, ",回归系数：", b)

    y_train_pred = model.predict(X_train)
    # 绘制最佳拟合线：标签用的是训练数据的预测值y_train_pred
    plt.plot(X_train, y_train_pred, color='black', linewidth=1, label="best line")

    # 测试数据散点图
    plt.scatter(X_test, Y_test, color='red', label="test data")

    # 添加图标标签
    plt.legend(loc=1)
    # 显示图像
    plt.show()

    score = model.score(X_test, Y_test)

    print(score)

def show_trend(a,b):
    examdict = {"a": a, "b": b}
    examDf = DataFrame(examdict)
    examDf.plot(x='a',y='b')
    plt.show()


def chajia():
    raw = [ abs(i-nasdata['c'][index])   for (index,i) in  enumerate(nasdata['o'])]
    x = raw[0:-1]
    y = raw[1::]

    show_relation(a=x,b=y)


def maxchajia():
    raw = [abs(i - nasdata['l'][index]) for (index, i) in enumerate(nasdata['h'])]
    x = raw[0:-1]
    y = raw[1::]

    show_relation(a=x, b=y)

def chajia_trend():
    raw = [abs(i - nasdata['o'][index]) for (index, i) in enumerate(nasdata['c'])]
    x = range(0,len(raw))
    y = raw

    show_trend(a=x,b=y)

def maxchajia_trend():
    raw = [abs(i - nasdata['l'][index]) for (index, i) in enumerate(nasdata['h'])]
    x = range(0,len(raw))
    y = raw

    show_trend(a=x,b=y)


def chajia_trend_or():
    raw = [(i - nasdata['o'][index]) for (index, i) in enumerate(nasdata['c'])][400:500]
    x = range(0,len(raw))
    y = raw

    show_trend(a=x,b=y)

def maxchajia_trend_or():
    raw = [abs(i - nasdata['l'][index])* (( nasdata['c'][index]-nasdata['o'][index] )>=0 and 1 or -1 )for (index,i) in enumerate(nasdata['h'])][400:500]
    x = range(0,len(raw))
    y = raw

    show_trend(a=x,b=y)
maxchajia_trend_or()